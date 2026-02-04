import re
from collections import Counter

# 1. *** YOUR ACTION REQUIRED HERE ***
# DELETE the placeholder text below, and PASTE your French text
# directly between the triple quotes (''' and ''').
TEXT_TO_ANALYZE = '''
Alors on 
Alors on 
Alors on 
Qui dit étude dit travail 
Qui dit taf te dit les thunes 
Qui dit argent dit dépenses 
Et qui dit crédit dit créance 
Qui dit dette te dit huissier 
Et lui dit assis dans la merde 
Qui dit amour dit les gosses 
Dit toujours et dit divorce 
Qui dit proches te dit deuils 
Car les problèmes ne viennent pas seuls 
Qui dit crise te dit monde 
Dit famine, dit tiers-monde 
Et qui dit fatigue dit réveil 
Encore sourd de la veille 
Alors on sort pour oublier tous les problèmes 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Et là tu te dis que c'est fini 
Car pire que ça ce serait la mort 
Quand tu crois enfin que tu t'en sors 
Quand y en a plus et ben y en a encore 
Est-ce la zik ou les problèmes? 
Les problèmes ou bien la musique 
Ça te prend les tripes, ça te prend la tête 
Et puis tu pries pour que ça s'arrête 
Mais c'est ton corps, c'est pas le ciel 
Alors tu te bouches plus les oreilles 
Et là tu cries encore plus fort 
Et ça persiste 
Alors on chante 
Alors on chante 
Alors on chante 
Alors on chante 
Et puis seulement quand c'est fini 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Alors on danse 
Et ben y en a encore 
Et ben y en a encore 
Et ben y en a encore 
Et ben y en a encore 
Et ben y en a encore 
'''
# ------------------------------------

def analyze_french_words(text):
    """
    Counts the total number of unique French words (excluding most punctuation, 
    but keeping contractions like l'amour) and returns a list of unique words
    sorted by frequency (most frequent first).
    
    Args:
        text (str): The input string containing French text.

    Returns:
        tuple: (count (int), frequency_list (list))
    """
    
    # 1. Aggressively clean the input string:
    # Removes all non-printable control characters (like the problematic ^@ or \x00) 
    # that often sneak in when pasting text on Pydroid3.
    cleaned_input = "".join(filter(str.isprintable, text))
    
    # 2. Tokenization and Normalization:
    # We use a Regular Expression (re) to find sequences of letters (a-z) and 
    # French accented characters (À-ÿ range in Unicode), and the apostrophe (').
    # This handles words like "été", "c'est", and "l'eau" correctly.
    # re.IGNORECASE ensures 'La' and 'la' are counted together.
    words = re.findall(r"[a-zÀ-ÿ']+", cleaned_input, re.IGNORECASE)
    
    # 3. Final Cleaning and Lowercasing:
    processed_words = []
    for word in words:
        word = word.lower()
        
        # Apply a basic filter: only keep words of length 1 if they contain an 
        # apostrophe (i.e., they are part of a contraction like 'l'). This prevents 
        # single letters that might be punctuation residue from being counted.
        if len(word) > 1 or "'" in word:
             processed_words.append(word)

    # 4. Count the frequency of each unique word.
    word_counts = Counter(processed_words)
    
    # 5. Determine the number of unique words.
    unique_count = len(word_counts)
    
    # 6. Sort the words by frequency (descending order).
    frequency_list = word_counts.most_common()
            
    return unique_count, frequency_list

if __name__ == "__main__":
    
    print("--- French Word Frequency Analysis Tool ---")
    
    # Use the text assigned directly in the file.
    final_text = TEXT_TO_ANALYZE.strip()
    
    if not final_text:
        print("Error: TEXT_TO_ANALYZE is empty. Please paste your text between the triple quotes at the top of the script.")
    else:
        # Calculate the result
        unique_count, frequency_list = analyze_french_words(final_text)

        # Print the results
        print(f"\nText analyzed:\n{final_text}")
        print("=" * 45)
        
        # Unique Word Count
        print(f"Total number of unique French words: {unique_count}\n")
        
        # Frequency List
        if frequency_list:
            print("Word Frequency List (Most Frequent First):")
            
            # Print the header
            print("-" * 35)
            print("{:<10} {:<15} {:<10}".format("Rank", "Word", "Count"))
            print("-" * 35)
            
            # Print each item in the sorted list
            for i, (word, count) in enumerate(frequency_list, 1):
                # Format for display
                display_word = f"'{word}'"
                print("{:<10} {:<15} {:<10}".format(i, display_word, count))
            print("-" * 35)
        else:
            print("No French words were found after filtering.")