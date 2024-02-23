from constants import SYMBOLS_TYPES, COMPOUNDS_SYMBOLS

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
        



def lexer(line, line_i):
    line = line.replace('\n', '')

    if(not line):
        return
   
    token = ''
    line += ' '
    first_type = get_type(line[0])
    found_tokens = []

    for i,char in enumerate(line):
        actual_char_type = get_type(char)

        if(first_type != actual_char_type):
            token_type = get_type(token)
            if(token_type and token or 
               (not token_type and check_token_characters(token))):
                found_tokens.append((token, token_type if token_type else get_type(token[0])))
            first_type = actual_char_type
            token = ''
            
        elif(first_type == 'symbols'):
            if(token):
                found_tokens.append((token, 'symbols'))
            first_type = actual_char_type
            token=''

        token += char

    print(found_tokens)
