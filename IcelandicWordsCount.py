import string
from collections import Counter
import re

# 1. *** YOUR ACTION REQUIRED HERE ***
# DELETE the placeholder text below, and PASTE your Icelandic text
# directly between the triple quotes (''' and ''').
TEXT_TO_ANALYZE = '''
Unz þrír kvámu ór því liði
Öflgir ok ástkir æsir at húsi,
Fundu á landi lítt megandi
Ask ok Emblu örlöglausa.
Önd þau ne áttu, óð þau ne höfðu,
Lá né læti né litu góða;
Önd gaf Óðinn, óð gaf Hœnir,
Lá gaf Lóðurr ok litu góða.
Lá gaf Lóðurr ok litu góða.
'''
# ------------------------------------

def analyze_icelandic_words(text):
    """
    Counts the total number of unique words (case-insensitive) and returns a list 
    of unique words sorted by frequency (most frequent first).
    
    Args:
        text (str): The input string containing Icelandic text.

    Returns:
        tuple: (unique_word_count (int), frequency_list (list))
    """
    
    # 1. Clean and normalize the input string:
    # Ensure all text is lowercase for case-insensitive counting (e.g., 'Epli' and 'epli' are the same word).
    normalized_text = text.lower()
    
    # 2. Tokenize the text into words:
    # Use a regex to find sequences of Icelandic letters (including special characters: æéúíóþáö).
    # The 'u' in the pattern ensures we capture all Icelandic characters.
    # Note: If your text contains numbers or non-standard characters you want to exclude, 
    # you might need to adjust this pattern.
    
    # This pattern finds sequences of characters that are NOT common separators (spaces, punctuation).
    # It's a quick way to split text into word-like units.
    # If a word has internal punctuation (like an apostrophe), it might be split.
    # We will use simple splitting for general purpose frequency counting:
    
    # Replace common punctuation with a space to ensure words are split properly
    # Note: We must include the Icelandic punctuation '.' ',' '!' '?'
    cleaned_text = normalized_text.replace('-', ' ')
    
    # Remove all standard punctuation (since we count words, not characters)
    for punc in string.punctuation:
        cleaned_text = cleaned_text.replace(punc, ' ')

    # Split the text by whitespace to get a list of words
    all_words = cleaned_text.split()
    
    # 3. Filter out any remaining empty strings or purely numerical tokens (if desired)
    filtered_words = [
        word for word in all_words 
        if word and not word.isdigit()
    ]
    
    # 4. Count the frequency of each unique word.
    word_counts = Counter(filtered_words)
    
    # 5. Determine the number of unique words.
    unique_count = len(word_counts)
    
    # 6. Sort the words by frequency (descending order).
    # Returns a list of (word, count) tuples.
    frequency_list = word_counts.most_common()
            
    return unique_count, frequency_list

if __name__ == "__main__":
    
    print("--- Icelandic Word Frequency Analysis Tool ---")
    
    final_text = TEXT_TO_ANALYZE.strip()
    
    if not final_text:
        print("Error: TEXT_TO_ANALYZE is empty. Please paste your text between the triple quotes at the top of the script.")
    else:
        # Calculate the result
        unique_count, frequency_list = analyze_icelandic_words(final_text)

        # Print the results
        print(f"\nText analyzed (first 50 chars): '{final_text[:50]}...'\n")
        print("=" * 40)
        
        # Unique Word Count
        print(f"Total number of unique words found: {unique_count}\n")
        
        # Frequency List
        if frequency_list:
            print("Word Frequency List (Most Frequent First):")
            
            # Print the header
            print("-" * 35)
            print("{:<10} {:<15} {:<10}".format("Rank", "Word", "Count"))
            print("-" * 35)
            
            # Print each item in the sorted list
            for i, (word, count) in enumerate(frequency_list, 1):
                # We limit the word length for clean printing
                display_word = f"'{word[:12]}'"
                print("{:<10} {:<15} {:<10}".format(i, display_word, count))
            print("-" * 35)
        else:
            print("No words were found after filtering.")
