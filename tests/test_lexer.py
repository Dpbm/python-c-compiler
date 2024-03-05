import unittest
from constants import DIRECTIVE, SYMBOLS, RESERVED, LETTERS, NUMBERS, SYMBOLS_TYPES
from lexer import get_type, check_token_characters, lexer_main
from itertools import product

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

class TestCheckTokenCharacters(unittest.TestCase):
    def test_empty_token(self):
        self.assertFalse(check_token_characters(""))
        self.assertFalse(check_token_characters(" "))
        self.assertFalse(check_token_characters("         "))
        self.assertFalse(check_token_characters("😃"))
    
    def test_one_char_token(self):
        self.assertTrue(check_token_characters("/"))
        self.assertTrue(check_token_characters("a"))
        self.assertTrue(check_token_characters("1"))
   
    def test_valid_token(self):
        self.assertTrue(check_token_characters("=="))
        self.assertTrue(check_token_characters("double"))
        self.assertTrue(check_token_characters("hello"))
        self.assertTrue(check_token_characters("int"))
        self.assertTrue(check_token_characters("/*"))
        self.assertTrue(check_token_characters("--"))

    def test_invalid_token(self):
        self.assertFalse(check_token_characters("^4"))
        self.assertFalse(check_token_characters("1dd32"))
        self.assertFalse(check_token_characters("ndndndndn-dd32"))
    
class TestLexerMain(unittest.TestCase):
    def test_plain_tokens(self):
        for symbol_type, symbols in SYMBOLS_TYPES.items():
            for symbol in symbols:
                self.assertEqual(lexer_main([symbol])[0][0][1], symbol_type)
    
    def test_distinguish_letters_next_to_symbols(self):
        for letter in LETTERS:
            for symbol_left, symbol_right in product(SYMBOLS, repeat=2):
                result = lexer_main([symbol_left+letter+symbol_right])
                self.assertEqual(result[0][0][1], 'symbols')
                self.assertEqual(result[0][1][1], 'letters')
                self.assertEqual(result[0][2][1], 'symbols')

    def test_distinguish_letters_next_to_directive(self):
        for letter in LETTERS:
            for directive_left, directive_right in product(DIRECTIVE, repeat=2):
                result = lexer_main([directive_left+letter+directive_right])
                self.assertEqual(result[0][0][1], 'directive')

if __name__ == '__main__':
    unittest.main()
