import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from collections import Counter
import re
import sys

# --- Configuration ---
INPUT_FILE = 'input_book.epub'
OUTPUT_FILE = 'gradual_french.epub'
CHUNK_SIZE = 100  # Number of words before picking a new translation
TARGET_LANG = 'fr'

translator = GoogleTranslator(source='en', target=TARGET_LANG)
replacement_dict = {}  # Global: English word -> French word
word_count_total = 0
chunk_buffer = []

def get_most_frequent_new_word(words):
    """Finds the most common word that isn't already in our dictionary."""
    counts = Counter(words)
    # Sort by frequency descending
    for word, count in counts.most_common():
        if word not in replacement_dict and len(word) > 1: # Ignore single letters
            return word
    return None

def process_text_node(node):
    global word_count_total, chunk_buffer
    
    original_text = str(node)
    # Use regex to find words (handling apostrophes like "don't")
    words_in_node = re.findall(r"\b[\w']+\b", original_text)
    
    for word in words_in_node:
        chunk_buffer.append(word.lower())
        word_count_total += 1
        
        # Every 100 words, trigger a new translation rule
        if len(chunk_buffer) >= CHUNK_SIZE:
            target = get_most_frequent_new_word(chunk_buffer)
            if target:
                try:
                    translated = translator.translate(target)
                    replacement_dict[target] = translated
                    print(f"[LOG] Word #{word_count_total}: Found '{target}' ({chunk_buffer.count(target)}x). Translated to '{translated}'")
                except Exception as e:
                    print(f"[ERROR] Translation failed for {target}: {e}")
            chunk_buffer = [] # Clear buffer for next 100

    # Apply all currently known replacements to this node
    new_text = original_text
    # Sort keys by length to prevent replacing parts of words
    for eng_word in sorted(replacement_dict.keys(), key=len, reverse=True):
        pattern = re.compile(r'\b' + re.escape(eng_word) + r'\b', re.IGNORECASE)
        # This preserves the original case of the French word from the translator
        new_text = pattern.sub(replacement_dict[eng_word], new_text)
    
    return new_text

def run_immersion_process():
    print(f"--- Starting Immersion Process ---")
    print(f"Input: {INPUT_FILE}")
    
    try:
        book = epub.read_epub(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found. Place the file in the Pydroid folder.")
        return

    new_book = epub.EpubBook()
    
    items = list(book.get_items())
    total_items = len([i for i in items if i.get_type() == ebooklib.ITEM_DOCUMENT])
    processed_count = 0

    for item in items:
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            processed_count += 1
            print(f"\n[CHAPTER] Processing {item.get_name()} ({processed_count}/{total_items})...")
            
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            # Process only visible text nodes
            for text_node in soup.find_all(string=True):
                if text_node.parent.name not in ['script', 'style', 'head', 'title']:
                    new_content = process_text_node(text_node)
                    text_node.replace_with(new_content)
            
            item.set_content(str(soup).encode('utf-8'))
        
        new_book.add_item(item)

    # Maintain EPUB structure
    new_book.toc = book.toc
    new_book.spine = book.spine
    new_book.metadata = book.metadata
    
    print(f"\n--- Finalizing File ---")
    epub.write_epub(OUTPUT_FILE, new_book)
    print(f"Success! {OUTPUT_FILE} created.")
    print(f"Total words processed: {word_count_total}")
    print(f"Total unique words French-ified: {len(replacement_dict)}")

if __name__ == "__main__":
    run_immersion_process()
