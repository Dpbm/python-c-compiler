import unittest
from constants import DIRECTIVE, SYMBOLS, RESERVED, LETTERS, NUMBERS
from lexer import get_type

class TestLexerGetType(unittest.TestCase):
    def test_get_directive(self):
        for directive in DIRECTIVE:
            self.assertEqual(get_type(directive), "directive")

    def test_get_symbols(self):
        for symbol in SYMBOLS:
            self.assertEqual(get_type(symbol), "symbols")
    
    def test_get_reserved(self):
        for reserved in RESERVED:
            self.assertEqual(get_type(reserved), "reserved")

    def test_get_letters(self):
        for letter in LETTERS:
            self.assertEqual(get_type(letter), "letters")

    def test_get_numbers(self):
        for number in NUMBERS:
            self.assertEqual(get_type(number), "numbers")

    def test_get_none(self):
        self.assertEqual(get_type("jdkl2!39jsd#"), None)

if __name__ == '__main__':
    unittest.main()
