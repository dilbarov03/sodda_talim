import string

def process_string(input_str):
    # Remove punctuation marks and convert to lowercase
    clean_str = ''.join(char.lower() for char in input_str if char.isalnum() or char.isspace())
    
    # Split the string into words, remove spaces, and join them into one word
    words = clean_str.split()
    result = ''.join(words)
    
    return result
