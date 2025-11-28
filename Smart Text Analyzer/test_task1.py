"""
Test suite for Task 1: Smart Text Analyzer
"""

import unittest
from task1_text_analyzer import analyze_text


class TestTextAnalyzer(unittest.TestCase):
    """Test cases for the text analyzer function."""
    
    def test_example_input(self):
        """Test with the provided example input."""
        text = "The quick brown fox jumps over the lazy dog the fox"
        result = analyze_text(text)
        
        # Note: Actual word count is 11 (task description says 10, which appears to be incorrect)
        # Words: The, quick, brown, fox, jumps, over, the, lazy, dog, the, fox
        self.assertEqual(result["word_count"], 11)
        # Average: (3+5+5+3+5+4+3+4+3+3+3)/11 = 41/11 ≈ 3.73
        self.assertAlmostEqual(result["average_word_length"], 3.73, places=2)
        self.assertIn("quick", result["longest_words"])
        self.assertIn("brown", result["longest_words"])
        self.assertIn("jumps", result["longest_words"])
        # "the" appears 3 times (The, the, the) - all lowercased
        self.assertEqual(result["word_frequency"]["the"], 3)
        # "fox" appears 2 times
        self.assertEqual(result["word_frequency"]["fox"], 2)
    
    def test_empty_string(self):
        """Test with empty string."""
        result = analyze_text("")
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["average_word_length"], 0.00)
        self.assertEqual(result["longest_words"], [])
        self.assertEqual(result["word_frequency"], {})
    
    def test_whitespace_only(self):
        """Test with whitespace only."""
        result = analyze_text("   \n\t  ")
        self.assertEqual(result["word_count"], 0)
    
    def test_single_word(self):
        """Test with single word."""
        result = analyze_text("Hello")
        self.assertEqual(result["word_count"], 1)
        self.assertEqual(result["average_word_length"], 5.00)
        self.assertEqual(result["longest_words"], ["hello"])
        self.assertEqual(result["word_frequency"]["hello"], 1)
    
    def test_case_insensitive(self):
        """Test that word frequency is case-insensitive."""
        result = analyze_text("Hello hello HELLO")
        self.assertEqual(result["word_frequency"]["hello"], 3)
    
    def test_punctuation_handling(self):
        """Test that punctuation is handled correctly."""
        result = analyze_text("Hello, world! How are you?")
        self.assertEqual(result["word_count"], 5)
        self.assertIn("hello", result["word_frequency"])
        self.assertIn("world", result["word_frequency"])
    
    def test_tied_longest_words(self):
        """Test that all tied longest words are returned."""
        result = analyze_text("a ab abc def ghi")
        self.assertIn("abc", result["longest_words"])
        self.assertIn("def", result["longest_words"])
        self.assertIn("ghi", result["longest_words"])
        self.assertEqual(len(result["longest_words"]), 3)


if __name__ == "__main__":
    unittest.main()

