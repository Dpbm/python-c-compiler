from constants import SYMBOLS_TYPES

def get_char_type(char):
    for s_type, s_set in SYMBOLS_TYPES.items():
        if(char in s_set):
            return s_type
    return None

def lexer(line, line_i):
    line = line.replace('\n', '')
        

    if(not line):
        return

    i = 0
    token = line[i]
    first_char_type = get_char_type(line[i])
    last_char_type = first_char_type

    while(True):
        i += 1
        last_char_type = get_char_type(line[i])
        if(first_char_type != last_char_type):
            break
        token += line[i]
    
    token_type = get_char_type(token)
    if(token_type == 'directive'):
        print(f'line: {line_i}, token: {token}, symbol type: {token_type}')
        return

