import unittest
from constants import OPEN_DIRECTIVE,DIRECTIVE_MULTIPLE_LINES_BEGIN, DIRECTIVE_MULTIPLE_LINES_END, DIRECTIVE_MULTIPLE_LINES,DIRECTIVE_ONE_LINE, DIRECTIVE, SYMBOLS, RESERVED, LETTERS, NUMBERS, SYMBOLS_TYPES
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
                self.assertEqual(len(result[0]), 1 if directive_left in OPEN_DIRECTIVE else 3)

    def test_distinguish_numbers_next_to_symbols(self):
        for number in NUMBERS:
            for symbol_left, symbol_right in product(SYMBOLS, repeat=2):
                result = lexer_main([symbol_left+number+symbol_right])
                self.assertEqual(result[0][0][1], 'symbols')
                self.assertEqual(result[0][1][1], 'numbers')
                self.assertEqual(result[0][2][1], 'symbols')
    
    def test_distinguish_numbers_next_to_directive(self):
        for number in NUMBERS:
            for directive_left, directive_right in product(DIRECTIVE, repeat=2):
                result = lexer_main([directive_left+number+directive_right])
                self.assertEqual(result[0][0][1], 'directive')
                self.assertEqual(len(result[0]), 1 if directive_left in OPEN_DIRECTIVE else 3)
    
    def test_distinguish_numbers_next_to_letters(self):
        for number in NUMBERS:
            for letter_left, letter_right in product(LETTERS, repeat=2):
                result = lexer_main([letter_left+number+letter_right])
                self.assertEqual(result[0][0][1], 'letters')
                self.assertEqual(result[0][1][1], 'numbers')
                self.assertEqual(result[0][2][1], 'letters')

    def test_distinguish_numbers_next_to_reserved_words(self):
        for number in NUMBERS:
            for reserved_left, reserved_right in product(RESERVED, repeat=2):
                result = lexer_main([reserved_left+number+reserved_right])
                self.assertEqual(result[0][0][1], 'reserved')
                self.assertEqual(result[0][1][1], 'numbers')
                self.assertEqual(result[0][2][1], 'reserved')
    
    def test_distinguish_directive_next_to_letters(self):
        for directive in DIRECTIVE:
            for letter_left, letter_right in product(LETTERS, repeat=2):
                result = lexer_main([letter_left+directive+letter_right])

                self.assertEqual(result[0][0][1], 'letters')
                self.assertEqual(result[0][1][1], 'directive')
                self.assertEqual(len(result[0]), 2 if directive in OPEN_DIRECTIVE else 3)

    def test_distinguish_directive_next_to_numbers(self):
        for directive in DIRECTIVE:
            for number_left, number_right in product(NUMBERS, repeat=2):
                result = lexer_main([number_left+directive+number_right])
                self.assertEqual(result[0][0][1], 'numbers')
                self.assertEqual(result[0][1][1], 'directive')
                self.assertEqual(len(result[0]), 2 if directive in OPEN_DIRECTIVE else 3)
    
    def test_distinguish_directive_next_to_symbols(self):
        for directive in DIRECTIVE:
            for symbol_left, symbol_right in product(SYMBOLS-{'/', '*'}, repeat=2):
                result = lexer_main([symbol_left+directive+symbol_right])
                self.assertEqual(result[0][0][1], 'symbols')
                self.assertEqual(result[0][1][1], 'directive')
                self.assertEqual(len(result[0]), 2 if directive in OPEN_DIRECTIVE else 3)
    
    def test_distinguish_directive_next_to_reserved_words(self):
        for directive in DIRECTIVE:
            for reserved_left, reserved_right in product(RESERVED, repeat=2):
                result = lexer_main([reserved_left+directive+reserved_right])
                self.assertEqual(result[0][0][1], 'reserved')
                self.assertEqual(result[0][1][1], 'directive')
                self.assertEqual(len(result[0]), 2 if directive in OPEN_DIRECTIVE else 3)

    def test_distinguish_reserved_next_to_symbols(self):
        for reserved in RESERVED:
            for symbol_left, symbol_right in product(SYMBOLS, repeat=2):
                result = lexer_main([symbol_left+reserved+symbol_right])
                self.assertEqual(result[0][0][1], 'symbols')
                self.assertEqual(result[0][1][1], 'reserved')
                self.assertEqual(result[0][2][1], 'symbols')
    
    def test_distinguish_reserved_next_to_numbers(self):
        for reserved in RESERVED:
            for number_left, number_right in product(NUMBERS, repeat=2):
                result = lexer_main([number_left+reserved+number_right])
                self.assertEqual(result[0][0][1], 'numbers')
                self.assertEqual(result[0][1][1], 'reserved')
                self.assertEqual(result[0][2][1], 'numbers')
    
    def test_distinguish_reserved_next_to_directive(self):
        for reserved in RESERVED:
            for directive_left, directive_right in product(DIRECTIVE, repeat=2):
                result = lexer_main([directive_left+reserved+directive_right])
                self.assertEqual(result[0][0][1], 'directive')
                self.assertEqual(len(result[0]), 1 if directive_left in OPEN_DIRECTIVE else 3)

    def test_distinguish_symbols_next_to_numbers(self):
        for symbol in SYMBOLS:
            for number_left, number_right in product(NUMBERS, repeat=2):
                result = lexer_main([number_left+symbol+number_right])
                self.assertEqual(result[0][0][1], 'numbers')
                self.assertEqual(result[0][1][1], 'symbols')
                self.assertEqual(result[0][2][1], 'numbers')
    
    def test_distinguish_symbols_next_to_letters(self):
        for symbol in SYMBOLS:
            for letter_left, letter_right in product(LETTERS, repeat=2):
                result = lexer_main([letter_left+symbol+letter_right])
                self.assertEqual(result[0][0][1], 'letters')
                self.assertEqual(result[0][1][1], 'symbols')
                self.assertEqual(result[0][2][1], 'letters')


    def test_distinguish_symbols_next_to_directives(self):
        for symbol in SYMBOLS-{'/', '*'}:
            for directive_left, directive_right in product(DIRECTIVE, repeat=2):
                result = lexer_main([directive_left+symbol+directive_right])
                self.assertEqual(result[0][0][1], 'directive')
                print(result, directive_right, symbol)
                if(directive_left == DIRECTIVE_MULTIPLE_LINES_BEGIN and directive_right == DIRECTIVE_MULTIPLE_LINES_END):
                    self.assertEqual(len(result[0]), 2)
                elif(directive_left in OPEN_DIRECTIVE):
                    self.assertEqual(len(result[0]), 1)
                else:
                    self.assertEqual(len(result[0]), 3)

if __name__ == '__main__':
    unittest.main()
