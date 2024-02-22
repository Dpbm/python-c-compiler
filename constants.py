from string import ascii_lowercase, ascii_uppercase, digits

LETTERS_LOWERCASE = set(ascii_lowercase.split())
LETTERS_UPPERCASE = set(ascii_uppercase.split())
LETTERS = set().union(LETTERS_LOWERCASE, LETTERS_UPPERCASE)

NUMBERS = set(digits.split())

DIRECTIVE_ONE_LINE = {'#', '//'}
DIRECTIVE_MULTIPLE_LINES = {'/*', '*/'}
SYMBOLS = {',', ';', '(', ')', '{', '}', "'", '"', '+', '-', ':', '%', '/', '*', '=', '==', '[',']'}
RESERVED = {'void', 'main', 'int', 'char', 'for', 'if', 'while', 'return', 'static', 'double', 'do', 'goto', 'auto', 'else', 'float'}

COMPOUNDS = {'//', '++', '--'}

DIRECTIVE = set().union(DIRECTIVE_ONE_LINE, DIRECTIVE_MULTIPLE_LINES)

SYMBOLS_TYPES = {
    "directive": DIRECTIVE,
    "symbols": SYMBOLS,
    "reserved": RESERVED,
    'letters': LETTERS,
    'numbers': NUMBERS
}

ALL_SYMBOLS = set().union(DIRECTIVE, SYMBOLS, RESERVED, LETTERS, NUMBERS)
