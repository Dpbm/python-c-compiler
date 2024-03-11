from string import ascii_uppercase, ascii_lowercase, digits

LETTERS = set(list(ascii_uppercase+ascii_lowercase))
NUMBERS = set(list(digits))

class Line:
    i = 0
    line = ''
    def __init__(self, line):
        self.line = line

    def __next__(self):
        if(self.i >= len(self.line)):
            return ''
        else:
            char_to_return = self.line[self.i]
            self.i += 1
            return char_to_return
    
    def __str__(self):
        return self.line[self.i]

    def get_next(self, n_i):
        return self.line[self.i+n_i] if (self.i+n_1 < len(self.line)) else ''

    def go_forward(self, steps):
        self.i += steps

    def get_atual_char(self):
        return self.line[self.i-1]

def lexer(source):
    tokens = []
    string_text_block = False
    char_text_block = False
    directive_block = False
    letters_block = False
    numbers_block = False
    text = ''

    for i,line in enumerate(source):
        actual_line = i+1
        l = Line(line)

        char = next(l)
            
        while(char):
            found_reserved = False
         
            if(string_text_block):
                if(char == '"'):
                    tokens.append((text, 'text', actual_line))
                    tokens.append(('"', 'symbol', actual_line))
                    string_text_block = False
                    text = ''
                else:            
                    text += char
                
                char = next(l)
                continue
            
            if(char_text_block):
                if(char == "'"):
                    tokens.append((text, 'text', actual_line))
                    tokens.append(("'", 'symbol', actual_line))
                    char_text_block = False
                    text = ''
                else:            
                    text += char

                char = next(l)
                continue

            if(directive_block):
                if(char == '*'):
                    if(next(l) == "/"):
                        tokens.append(('*/', 'directive', actual_line))
                        directive_block = False
                char = next(l)
                continue

            if(letters_block):
                if(char not in LETTERS):               
                    letters_block = False
                    tokens.append((text, 'letters', actual_line))
                    text = ''
                else:
                    text += char
                    char = next(l)
                    continue
            
            if(numbers_block):
                if(char not in NUMBERS):               
                    numbers_block = False
                    tokens.append((text, 'numbers', actual_line))
                    text = ''
                else:
                    text += char
                    char = next(l)
                    continue

            # symbols and directives
            if(not char or char in {'\t', '\n', ' '}):
                char = next(l)
                continue

            elif(char == '#'):
                tokens.append((char, 'directive', actual_line))
                break

            elif(char in {'{', '}', ',', ';', '(', ')', '[', ']'}):
                tokens.append((char, 'symbol', actual_line))
       
            elif(char == '='):
                tokens.append(('==' if next(l)=='=' else '=', 'symbol', actual_line))
                
            elif(char == '+'):
                next_char = next(l)

                if(next_char == '='):
                    tokens.append(('+=', 'symbol', actual_line))
                elif(next_char == '+'):
                    tokens.append(('++', 'symbol', actual_line))
                else:
                    tokens.append(('+', 'symbol', actual_line))
            
            elif(char == '-'):
                next_char = next(l)

                if(next_char == '='):
                    tokens.append(('-=', 'symbol', actual_line))
                elif(next_char == '-'):
                    tokens.append(('--', 'symbol', actual_line))
                else:
                    tokens.append(('-', 'symbol', actual_line))

            elif(char == '*'):
                next_char = next(l)

                if(next_char == '='):
                    tokens.append(('*=', 'symbol', actual_line))
                elif(next_char == '*'):
                    tokens.append(('**', 'symbol', actual_line))
                else:
                    tokens.append(('*', 'symbol', actual_line))
                
            elif(char == '/'):
                next_char = next(l)

                if(next_char == '/'):
                    tokens.append(('//', 'directive', actual_line))
                    break;
                elif(next_char == '='):
                    tokens.append(('/=', 'symbol', actual_line))
                elif(next_char == '*'):
                    tokens.append(('/*', 'directive', actual_line))
                    directive_block = True
                else:
                    tokens.append(('/', 'symbol', actual_line))

            elif(char == '<'):
                tokens.append(('<=' if next(l)=='=' else '<', 'symbol', actual_line))
            
            elif(char == '>'):
                tokens.append(('>=' if next(l)=='=' else '>', 'symbol', actual_line))

            elif(char == "'"):
                tokens.append(("'", 'symbol', actual_line))
                char_text_block = True

            elif(char == '"'):
                tokens.append(('"', 'symbol', actual_line))
                string_text_block = True


            # reserved
            elif(char == 'm'):
                found_reserved = check_reserved(l, {'main'})
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))
            
            elif(char == 'e'):
                found_reserved = check_reserved(l, {'else'})
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))

            elif(char == 'i'):
                reserved_starting_with_i = {'int', 'if'}
                found_reserved = check_reserved(l, reserved_starting_with_i)
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))
            
            elif(char == 'p'):
                found_reserved = check_reserved(l, {'printf'})
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))

            elif(char == 'f'):
                reserved_starting_with_f = {'float', 'for'}
                found_reserved = check_reserved(l, reserved_starting_with_f)
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))
            
            if(not found_reserved and char in LETTERS):
                letters_block = True
                continue
            
            if(char in NUMBERS):
                numbers_block = True
                continue

            char = next(l)

    return tokens

def check_reserved(line, reserved_words):
    j = 0
    larger_word = len(max(reserved_words)) 
    token = line.get_atual_char()+line.get_next(1)

    while(j < larger_word and token not in reserved_words):
        j+=1
        token += line.get_next(j)

    if(token in reserved_words):
        reserved_words_list = list(reserved_words)
        line.go_forward(j+1)
        return reserved_words_list[reserved_words_list.index(token)]
    else:
        line.reset(j)
        return ''
