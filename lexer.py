from constants import SYMBOLS_TYPES, COMPOUNDS

def get_type(char):
    for s_type, s_set in SYMBOLS_TYPES.items():
        if(char in s_set):
            return s_type
    return None

def parse_token(line, i):
    if(len(line)-1 == i and not line[i]):
        return('', None, i)

    token = line[i]
    first_char_type = get_type(line[i])
    last_char_type = first_char_type
    
    while(True):
        
        i += 1  
        last_char_type = get_type(line[i])
        if(last_char_type == 'symbols' and token+line[i] not in COMPOUNDS):
            break
       
        if(line[i] == ' '):
            i += 1
            break

        if(first_char_type != last_char_type):
            break
        token += line[i]

    token_type = get_type(token)

    return (token, token_type, i)

def lexer(line, line_i):
    line = line.replace('\n', '')

    if(not line):
        return

    line += ' '
    i = 0
    while(i < len(line)):
        token, token_type, i = parse_token(line, i) 

        if(token):
            print(f'line: {line_i}, token: {token}, symbol type: {token_type}')
        if(token_type == 'directive'):
            break
