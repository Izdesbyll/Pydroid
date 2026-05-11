import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from collections import Counter
import re

def rewrite_epub_with_translation(input_path, output_path, threshold=5):
    translator = GoogleTranslator(source='en', target='no')
    global_word_counts = Counter()
    translation_cache = {}

    print(f"Loading {input_path}...")
    book = epub.read_epub(input_path)
    new_book = epub.EpubBook()
    new_book.metadata = book.metadata
    
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            
            for text_node in soup.find_all(string=True):
                if text_node.parent.name in ['script', 'style']:
                    continue
                
                segments = re.findall(r"[\w']+|[^\w']+", text_node.string)
                new_segments = []
                
                for segment in segments:
                    if re.match(r"[\w']+", segment):
                        word_lower = segment.lower()
                        global_word_counts[word_lower] += 1
                        
                        if global_word_counts[word_lower] > threshold:
                            if word_lower not in translation_cache:
                                try:
                                    translated = translator.translate(word_lower)
                                    # FIX: Only cache if translated is a valid string
                                    if translated and isinstance(translated, str):
                                        translation_cache[word_lower] = translated
                                        print(f"Translated: {word_lower} -> {translated}")
                                    else:
                                        translation_cache[word_lower] = segment
                                except Exception:
                                    translation_cache[word_lower] = segment
                            
                            target_word = translation_cache[word_lower]
                            
                            # Double check target_word is a string before formatting
                            if isinstance(target_word, str):
                                if segment.isupper():
                                    new_segments.append(target_word.upper())
                                elif segment[0].isupper():
                                    new_segments.append(target_word.capitalize())
                                else:
                                    new_segments.append(target_word.lower())
                            else:
                                new_segments.append(segment)
                        else:
                            new_segments.append(segment)
                    else:
                        new_segments.append(segment)
                
                text_node.replace_with("".join(new_segments))
            
            item.set_content(str(soup).encode('utf-8'))
        
        new_book.add_item(item)

    new_book.spine = book.spine
    new_book.toc = book.toc
    
    print("Saving file...")
    epub.write_epub(output_path, new_book)
    print(f"Done! Created: {output_path}")

# Run it
rewrite_epub_with_translation('input_book.epub', 'output_bokmal.epub')
