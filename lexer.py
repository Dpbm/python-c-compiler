from constants import DIRECTIVE_ONE_LINE, SYMBOLS_TYPES, COMPLETE_COMPOUND_SYMBOLS, COMPOUNDS_SYMBOLS, DIRECTIVE_MULTIPLE_LINES_BEGIN, DIRECTIVE_MULTIPLE_LINES_END

def get_type(char):
    for s_type, s_set in SYMBOLS_TYPES.items():
        if(char in s_set):
            return s_type
    return None

def check_token_characters(token):
    if(not len(token) or not get_type(token[0])):
        return False
    
    first_char_type = get_type(token[0])
    for char in token:
        if(get_type(char) != first_char_type):
            return False
    return True

def lexer_main(file):
    directive_multiple_lines = False
    tokens_table = []
    
    for i in range(len(file)):
        tokens,directive_multiple_lines = lexer(file[i],directive_multiple_lines)
        if(tokens):
            tokens_table.append(tokens)
    return tokens_table


def lexer(line, directive_multiple_lines=False):
    line = line.replace('\n', '')

    if(not line):
        return [], False
   
    token = ''
    line += ' '
    first_type = get_type(line[0])
    found_tokens = []
    string = False

    for i,char in enumerate(line):
        actual_char_type = get_type(char)
       
        if(string):
            if(char == '"'):
                string=False
                found_tokens.append((token, 'text'))
            else:
                token += char
                continue



        if(first_type != actual_char_type):
            token_type = get_type(token)
            if((token_type and token) or 
               (not token_type and check_token_characters(token))):                

                if(token == '"' and not string):
                    string = True


                if(directive_multiple_lines and token != DIRECTIVE_MULTIPLE_LINES_END):
                    continue

                found_tokens.append((token, token_type if token_type else get_type(token[0])))
                
                
                if(token == DIRECTIVE_MULTIPLE_LINES_BEGIN):
                    directive_multiple_lines = True
                elif(token == DIRECTIVE_MULTIPLE_LINES_END):
                    directive_multiple_lines = False

                if(token_type == 'directive' and token in DIRECTIVE_ONE_LINE):
                    break

            first_type = actual_char_type
            token = ''
        
        elif(first_type == 'symbols' and token in COMPLETE_COMPOUND_SYMBOLS):
            if(not directive_multiple_lines and token in DIRECTIVE_ONE_LINE):    
                found_tokens.append((token, get_type(token)))
                break
            
            if((directive_multiple_lines and token==DIRECTIVE_MULTIPLE_LINES_END) or
               (not directive_multiple_lines and token == DIRECTIVE_MULTIPLE_LINES_BEGIN) or 
               (not directive_multiple_lines)
               ):
                found_tokens.append((token, get_type(token)))
                first_type = actual_char_type

            if(token == DIRECTIVE_MULTIPLE_LINES_BEGIN):
                directive_multiple_lines = True
            elif(token == DIRECTIVE_MULTIPLE_LINES_END):
                directive_multiple_lines = False
            

            token=''
            

        elif(first_type == 'symbols' and (token not in COMPOUNDS_SYMBOLS or token+char not in COMPLETE_COMPOUND_SYMBOLS) and not directive_multiple_lines):
            if(token):
                found_tokens.append((token, 'symbols'))
            first_type = actual_char_type
            token=''

        token += char

    return found_tokens, directive_multiple_lines
