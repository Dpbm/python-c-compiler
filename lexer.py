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

    def reset(self, steps):
        self.i -= steps+1

    def get_atual_char(self):
        return self.line[self.i-1]

def lexer(source):
    tokens = []
    for i,line in enumerate(source):
        actual_line = i+1
        l = Line(line)

        char = next(l)
            
        while(char):
            if(char == '#'):
                tokens.append((char, 'directive', actual_line))
                break

            elif(char in {'{', '}', ',', ';', '(', ')', '[', ']'}):
                tokens.append((char, 'symbol', actual_line))
       
            elif(char == 'm'):
                if(check_reserved(l, {'main'})): 
                    tokens.append(('main', 'reserved', actual_line))
            
            elif(char == 'e'):
                if(check_reserved(l, {'else'})): 
                    tokens.append(('else', 'reserved', actual_line))

            elif(char == 'i'):
                reserved_starting_with_i = {'int', 'if'}
                found_reserved = check_reserved(l, reserved_starting_with_i)
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))
            
            elif(char == 'p'):
                if(check_reserved(l, {'printf'})): 
                    tokens.append(('printf', 'reserved', actual_line))

            elif(char == 'f'):
                reserved_starting_with_f = {'float', 'for'}
                found_reserved = check_reserved(l, reserved_starting_with_f)
                if(found_reserved): 
                    tokens.append((found_reserved, 'reserved', actual_line))
            
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

            elif(char == '<'):
                tokens.append(('<=' if next(l)=='=' else '<', 'symbol', actual_line))

            char = next(l)

    return tokens

def check_reserved(line, reserved_words):
    j = 0
    larger_word = len(max(reserved_words)) 
    token = line.get_atual_char()+next(line)

    while(j < larger_word and token not in reserved_words):
        j+=1
        token += next(line)

    if(token in reserved_words):
        reserved_words_list = list(reserved_words)
        return reserved_words_list[reserved_words_list.index(token)]
    else:
        line.reset(j)
        return ''
