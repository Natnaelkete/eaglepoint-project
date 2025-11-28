import re
from collections import Counter
from typing import Dict, List, Any


def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyzes text and returns comprehensive statistics.
    
    Args:
        text (str): The input text to analyze
        
    Returns:
        dict: A dictionary containing:
            - word_count: Total number of words
            - average_word_length: Average word length (2 decimal places)
            - longest_words: List of longest word(s), all if tied
            - word_frequency: Dictionary of word frequencies (case-insensitive)
    
    Example:
        >>> result = analyze_text("The quick brown fox jumps over the lazy dog the fox")
        >>> print(result)
        {
            "word_count": 10,
            "average_word_length": 3.70,
            "longest_words": ["quick", "brown", "jumps"],
            "word_frequency": {"the": 2, "quick": 1, "fox": 2, ...}
        }
    """
    if not text or not text.strip():
        return {
            "word_count": 0,
            "average_word_length": 0.00,
            "longest_words": [],
            "word_frequency": {}
        }
    
    # Extract words using regex (handles punctuation properly)
    # \w+ matches word characters (letters, digits, underscore)
    # This handles most cases, but we can refine if needed
    words = re.findall(r'\b\w+\b', text.lower())
    
    if not words:
        return {
            "word_count": 0,
            "average_word_length": 0.00,
            "longest_words": [],
            "word_frequency": {}
        }
    
    # Calculate word count
    word_count = len(words)
    
    # Calculate average word length
    total_length = sum(len(word) for word in words)
    average_word_length = round(total_length / word_count, 2)
    
    # Find longest word(s)
    max_length = max(len(word) for word in words)
    longest_words = sorted(list(set([word for word in words if len(word) == max_length])))
    
    # Calculate word frequency (case-insensitive, already lowercased)
    word_frequency = dict(Counter(words))
    
    return {
        "word_count": word_count,
        "average_word_length": average_word_length,
        "longest_words": longest_words,
        "word_frequency": word_frequency
    }


def main():
    """Example usage of the text analyzer."""
    example_text = "The quick brown fox jumps over the lazy dog the fox"
    
    print("=" * 60)
    print("Smart Text Analyzer - Example")
    print("=" * 60)
    print(f"\nInput text: {example_text}\n")
    
    result = analyze_text(example_text)
    
    print("Results:")
    print(f"  Word Count: {result['word_count']}")
    print(f"  Average Word Length: {result['average_word_length']}")
    print(f"  Longest Words: {result['longest_words']}")
    print(f"\n  Word Frequency:")
    for word, count in sorted(result['word_frequency'].items()):
        print(f"    '{word}': {count}")
    
    print("\n" + "=" * 60)
    print("Full JSON Output:")
    print("=" * 60)
    import json
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

