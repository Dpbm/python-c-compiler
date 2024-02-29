from constants import SYMBOLS_TYPES, COMPOUNDS_SYMBOLS, DIRECTIVE_MULTIPLE_LINES_BEGIN, DIRECTIVE_MULTIPLE_LINES_END

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
    i=1
    directive_multiple_lines = False
    line = file.readline()
    tokens_table = []
    
    while(line):
        tokens,directive_multiple_lines = lexer(line,i, directive_multiple_lines)
        line = file.readline()
        i += 1
        if(tokens):
            tokens_table.append(tokens)
    print(tokens_table)


def lexer(line, line_i, directive_multiple_lines=False):
    line = line.replace('\n', '')

    if(not line):
        return [], False
   
    token = ''
    line += ' '
    first_type = get_type(line[0])
    found_tokens = []


    for i,char in enumerate(line):
        actual_char_type = get_type(char)


        if(first_type != actual_char_type):
            token_type = get_type(token)
            
            if((token_type and token) or 
               (not token_type and check_token_characters(token))):
                
                if(directive_multiple_lines and token != DIRECTIVE_MULTIPLE_LINES_END):
                    continue

                found_tokens.append((token, token_type if token_type else get_type(token[0])))
                
                if(token == DIRECTIVE_MULTIPLE_LINES_BEGIN):
                    directive_multiple_lines = True
                elif(token == DIRECTIVE_MULTIPLE_LINES_END):
                    directive_multiple_lines = False


            first_type = actual_char_type
            token = ''
            
        elif(first_type == 'symbols' and token not in COMPOUNDS_SYMBOLS):
            if(token):
                found_tokens.append((token, 'symbols'))
            first_type = actual_char_type
            token=''

        token += char

    return found_tokens, directive_multiple_lines
