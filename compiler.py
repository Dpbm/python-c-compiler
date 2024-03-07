import sys
import os
from lexer import lexer_main

def main(file):
    tokens = lexer_main(file.read().splitlines())

    for i, tokens_list in enumerate(tokens):
        for token in tokens_list: 
            print('linha: ', i+1, ' token: ', token[0], ' tipo: ', token[1])

if __name__ == "__main__":
    arguments = sys.argv

    if(len(arguments) != 2):
        print("Usage: python compiler.py input_file")
        sys.exit(1)

    input_file = arguments[-1]

    if(not os.path.exists(input_file)):
        print("File not found!")
        sys.exit(1)

    with open(input_file, "r") as file:
        main(file)
