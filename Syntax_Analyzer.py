import sys
import queue
import Lexer
from collections import deque

def main():
    print('im the SA!')
    tokens = []
    lexemes = []
    
    tokens, lexemes = Lexer.main()
    print(tokens)
    print(lexemes)


if __name__ == '__main__':
    main()