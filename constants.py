from string import ascii_lowercase, ascii_uppercase, digits

LETTERS_LOWERCASE = set(list(ascii_lowercase))
LETTERS_UPPERCASE = set(list(ascii_uppercase))
LETTERS = set().union(LETTERS_LOWERCASE, LETTERS_UPPERCASE)

NUMBERS = set(list(digits))

DIRECTIVE_ONE_LINE = {'#', '//'}
DIRECTIVE_MULTIPLE_LINES_BEGIN = '/*'
DIRECTIVE_MULTIPLE_LINES_END = '*/'
DIRECTIVE_MULTIPLE_LINES = {DIRECTIVE_MULTIPLE_LINES_BEGIN, DIRECTIVE_MULTIPLE_LINES_END}
SYMBOLS = {',', ';', '(', ')', '{', '}', "'", '"', '+', '-', ':', '%', '/', '*', '=', '==', '[',']'}
RESERVED = {'void', 'main', 'int', 'char', 'for', 'if', 'while', 'return', 'static', 'double', 'do', 'goto', 'auto', 'else', 'float'}

COMPOUNDS_SYMBOLS = {'/', '+', '-', '*'}

DIRECTIVE = set().union(DIRECTIVE_ONE_LINE, DIRECTIVE_MULTIPLE_LINES)

SYMBOLS_TYPES = {
    "directive": DIRECTIVE,
    "symbols": SYMBOLS,
    "reserved": RESERVED,
    'letters': LETTERS,
    'numbers': NUMBERS
}

ALL_SYMBOLS = set().union(DIRECTIVE, SYMBOLS, RESERVED, LETTERS, NUMBERS)
