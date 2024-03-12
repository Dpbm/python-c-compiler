from string import ascii_uppercase, ascii_lowercase, digits

LETTERS = set(list(ascii_uppercase+ascii_lowercase))
NUMBERS = set(list(digits))

class Line:
    i = 0
    line = ''
    def __init__(self, line):
        self.line = line

    def get_next(self, n_i):
        return self.line[self.i+n_i] if (self.i+n_i < len(self.line)) else ''

    def go_forward(self, steps):
        self.i += steps

    def get_actual_char(self):
        if(self.i >= len(self.line)):
            return None
        return self.line[self.i]

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

            
        while(l.get_actual_char()):
            found_reserved = False
            char = l.get_actual_char()
         
            if(string_text_block):
                if(char == '"'):
                    tokens.append((text, 'text', actual_line))
                    tokens.append(('"', 'symbol', actual_line))
                    string_text_block = False
                    text = ''
                else:            
                    text += char
                
                l.go_forward(1)
                continue
            
            if(char_text_block):
                if(char == "'"):
                    tokens.append((text, 'text', actual_line))
                    tokens.append(("'", 'symbol', actual_line))
                    char_text_block = False
                    text = ''
                else:            
                    text += char
                l.go_forward(1)
                continue

            if(directive_block):
                if(char == '*'):
                    if(l.get_next(1) == "/"):
                        tokens.append(('*/', 'directive', actual_line))
                        directive_block = False
                        l.go_forward(1)
                l.go_forward(1)
                continue

            if(letters_block):
                if(char not in LETTERS):               
                    letters_block = False
                    tokens.append((text, 'letters', actual_line))
                    text = ''
                else:
                    text += char
                    l.go_forward(1)
                    continue
            
            if(numbers_block):
                if(char not in NUMBERS):               
                    numbers_block = False
                    tokens.append((text, 'numbers', actual_line))
                    text = ''
                else:
                    text += char
                    l.go_forward(1)
                    continue

            # symbols and directives
            if(not char or char in {'\t', '\n', ' '}):
                l.go_forward(1)
                continue

            elif(char == '#'):
                tokens.append((char, 'directive', actual_line))
                break

            elif(char in {'{', '}', ',', ';', '(', ')', '[', ']'}):
                tokens.append((char, 'symbol', actual_line))
       
            elif(char == '='):
                if(l.get_next(1) == '='):
                    tokens.append(('==', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('=', 'symbol', actual_line))
                
            elif(char == '+'):
                next_char = l.get_next(1)

                if(next_char == '='):
                    tokens.append(('+=', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                elif(next_char == '+'):
                    tokens.append(('++', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('+', 'symbol', actual_line))
            
            elif(char == '-'):
                next_char = l.get_next(1)

                if(next_char == '='):
                    tokens.append(('-=', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                elif(next_char == '-'):
                    tokens.append(('--', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('-', 'symbol', actual_line))

            elif(char == '*'):
                next_char = l.get_next(1)

                if(next_char == '='):
                    tokens.append(('*=', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                elif(next_char == '*'):
                    tokens.append(('**', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('*', 'symbol', actual_line))
                
            elif(char == '/'):
                next_char = l.get_next(1)

                if(next_char == '/'):
                    tokens.append(('//', 'directive', actual_line))
                    break
                elif(next_char == '='):
                    tokens.append(('/=', 'symbol', actual_line))
                    l.go_forward(2)
                    continue
                elif(next_char == '*'):
                    tokens.append(('/*', 'directive', actual_line))
                    l.go_forward(2)
                    directive_block = True
                    continue
                else:
                    tokens.append(('/', 'symbol', actual_line))

            elif(char == '<'):
                if(l.get_next(1) == '='):
                    tokens.append(('<=', 'symbol' ,actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('<', 'symbol', actual_line))
            
            elif(char == '>'):
                if(l.get_next(1) == '='):
                    tokens.append(('>=', 'symbol' ,actual_line))
                    l.go_forward(2)
                    continue
                else:
                    tokens.append(('>', 'symbol', actual_line))

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
           
            print(line, char, l.get_next(-1), found_reserved, char in LETTERS)

            if(not found_reserved and char in LETTERS):
                letters_block = True
                continue
            
            if(char in NUMBERS):
                numbers_block = True
                continue

            l.go_forward(1)
    return tokens

def check_reserved(line, reserved_words):
    j = 0
    larger_word = len(max(reserved_words)) 
    token = line.get_actual_char()+line.get_next(1)

    while(j < larger_word and token not in reserved_words):
        j+=1
        token += line.get_next(j)

    if(token in reserved_words):
        reserved_words_list = list(reserved_words)
        line.go_forward(j+1)
        return reserved_words_list[reserved_words_list.index(token)]
    else:
        return ''
