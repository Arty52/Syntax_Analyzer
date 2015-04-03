import sys
import queue
import Lexer
from collections import deque

class Lex:
    def __init__(self, token, lexeme):
        self._token = token
        self._lexeme = lexeme
    
    #token get/set/property
    def setToken(self, token):
        self._token = token
    def getToken(self):
        return self._token
    token = property(getToken, setToken)
    
    #lexeme get/set/property
    def setLexeme(self, lexeme):
        self._lexeme = lexeme
    def getLexeme(self):
        return self._lexeme
    lexeme = property(getLexeme, setLexeme)
    

def expect(expected):
    print('\nERROR: SA expected: {}'.format(expected))
    print('Found: {}\n'.format())
    

def main():
#    bool print_production = True            #toggles print feature for the SA production
    print('im the SA!')
    tokens = []
    lexemes = []
    toProcess = deque()
    
    tokens, lexemes = Lexer.main()
    for i in range(len(tokens)):
        lex = Lex(tokens[i], lexemes[i])
        toProcess.append(lex)
    
    print('printing tokens from deque')
    for i in range(len(toProcess)):
        print(toProcess[i].token)
    print('printing lexemes from deque')
    for i in range(len(toProcess)):
        print(toProcess[i].lexeme)

    print(tokens)
    print(lexemes)


if __name__ == '__main__':
    main()