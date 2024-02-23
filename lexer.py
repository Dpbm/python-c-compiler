from constants import SYMBOLS_TYPES, COMPOUNDS_SYMBOLS

def get_type(char):
    for s_type, s_set in SYMBOLS_TYPES.items():
        if(char in s_set):
            return s_type
    return None

def lexer(line, line_i):
    line = line.replace('\n', '')

    if(not line):
        return
    
    found_tokens = []
    token = ''
    line += ' '
    

    for i,char in enumerate(line):
        if(char == ' ' and i != len(line)-1):
            continue
        
        token_type = get_type(token)

        if(token_type == 'directive'):
            found_tokens.append((token, token_type))
            break
        elif(token_type == 'reserved'  or 
             (token_type == 'symbols' and 
              token not in COMPOUNDS_SYMBOLS)):
            found_tokens.append((token, token_type))
            token=''

        # elif(len(token) and
        #      get_type(token[0]) == 'letters' and 
        #      get_type(token[-1]) == 'letters' and
        #      get_type(char) not in [None, 'letters']):
        #     found_tokens.append((token, token_type))
        #     token=''
        
        token += char
    print(found_tokens)
