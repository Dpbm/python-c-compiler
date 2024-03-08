import sys
import os
from lexer import lexer

def main(file):
    tokens = lexer(file.read().splitlines())
    for token, token_type, position in tokens:
        print(f'token: {token}  type: {token_type}  line: {position}')

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
