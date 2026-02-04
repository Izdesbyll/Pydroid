import string
from collections import Counter

# 1. *** YOUR ACTION REQUIRED HERE ***
# DELETE the placeholder text below, and PASTE your Chinese text
# directly between the triple quotes (''' and ''').
TEXT_TO_ANALYZE = '''
該不該擱下重重的殼　
尋找到底哪裡有藍天
隨著輕輕的風輕輕的飄　
歷經的傷都不感覺疼
 
我要一步一步往上爬　
等待陽光靜靜看著它的臉
小小的天有大大的夢想
重重的殼裹著輕輕的仰望
 
我要一步一步往上爬　
在最高點乘著葉片往前飛
小小的天流過的淚和汗　
總有一天我有屬於我的天
 
我要一步一步往上爬　
在最高點乘著葉片往前飛
任風吹乾流過的淚和汗
 
我要一步一步往上爬　
等待陽光靜靜看著它的臉
小小的天有大大的夢想
我有屬於我的天
 
任風吹乾流過的淚和汗　
總有一天我有屬於我的天
'''
# ------------------------------------

def analyze_chinese_symbols(text):
    """
    Counts the total number of unique symbols and returns a list of unique symbols
    sorted by frequency (most frequent first).
    
    Args:
        text (str): The input string containing Chinese and possibly other characters.

    Returns:
        tuple: (count (int), frequency_list (list))
    """
    
    # 1. Aggressively clean the input string:
    # Remove ALL non-printable control characters (\x00, etc.) that can cause issues in Pydroid3/Android.
    cleaned_input = "".join(filter(str.isprintable, text))
    
    # 2. Define characters to ignore: standard ASCII and common full-width Chinese punctuation.
    ignored_chars = string.whitespace + string.punctuation + "　" + "（）「」『』，《。》？！"
    
    # 3. Filter the text, keeping only the symbols we want to count/analyze.
    # We use a list comprehension for efficiency.
    filtered_symbols = [
        char for char in cleaned_input 
        if char not in ignored_chars
    ]
    
    # 4. Count the frequency of each unique symbol.
    symbol_counts = Counter(filtered_symbols)
    
    # 5. Determine the number of unique symbols (the size of the Counter).
    unique_count = len(symbol_counts)
    
    # 6. Sort the symbols by frequency (descending order).
    # counter.most_common() returns a list of (symbol, count) tuples, 
    # already sorted from most common to least common.
    frequency_list = symbol_counts.most_common()
            
    return unique_count, frequency_list

if __name__ == "__main__":
    
    print("--- Chinese Symbol Analysis Tool ---")
    
    # Use the text assigned directly in the file.
    final_text = TEXT_TO_ANALYZE.strip()
    
    if not final_text:
        print("Error: TEXT_TO_ANALYZE is empty. Please paste your text between the triple quotes at the top of the script.")
    else:
        # Calculate the result
        unique_count, frequency_list = analyze_chinese_symbols(final_text)

        # Print the results
        print(f"\nText analyzed: '{final_text}'")
        print("=" * 40)
        
        # Unique Symbol Count
        print(f"Total number of unique Chinese symbols: {unique_count}\n")
        
        # Frequency List
        if frequency_list:
            print("Symbol Frequency List (Most Frequent First):")
            
            # Print the header
            print("-" * 35)
            print("{:<10} {:<10} {:<10}".format("Rank", "Symbol", "Count"))
            print("-" * 35)
            
            # Print each item in the sorted list
            for i, (symbol, count) in enumerate(frequency_list, 1):
                print("{:<10} {:<10} {:<10}".format(i, f"'{symbol}'", count))
            print("-" * 35)
        else:
            print("No Chinese symbols were found after filtering.")
            