import sys
import queue
import Lexer
from collections import deque

#TODO, If there is time, move this to the Lexer.py program and have it return the deque containing the objects of Lex instead of just two lists.
class Lex:
    def __init__(self, token = None, lexeme = None):
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
    
#Global Variables
print_production = True            #toggles print feature for the SA production
toProcess = deque()
current = Lex()
error = True

#set current to the next variable to process
def getNext():
    if(toProcess):                          #if not empty
        current = toProcess.popleft()
        printInfo()

def printInfo():
    if(current):
        if(print_production):
            print('Token: {0:14} Lexeme: {1:1}'.format(current.token, current.lexeme))
    else:
        print('ERROR: current is empty')
    
####  Production Rules  ####
#<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> 
def rat15S():
    #initial production
    if(print_production):
        print('<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> ')
    
    # getNext()
    # if(optFunctionDefinitions()):
    #     getNext()
    #
    #     if (current.lexeme == '@@'):
    #         getNext()
    #         optDeclarationList()
    #     else:
    #         print('ERROR: expected @@')
    #
    # else:
    #     print('ERROR: Opt Function Definitions expected')
    
    
    
        
 
#<Opt Function Definitions> ::= <Function Definitions> | <Empty>
#<Function Definitions>  ::= <Function> | <Function> <Function Definitions>   
#<Function> ::= function  <Identifier> [ <Opt Parameter List> ]   <Opt Declaration List>  <Body>
# <Opt Parameter List> ::=  <Parameter List>   |  <Empty>
# <Parameter List>  ::=  <Parameter>  | <Parameter> , <Parameter List>
# <Parameter> ::=  <IDs > : <Qualifier>
# <Qualifier> ::= int   |  boolean  |  real
# <Body>  ::=  {  < Statement List>  }
# <Opt Declaration List> ::= <Declaration List>   | <Empty>
# <Declaration List>  := <Declaration> ;  | <Declaration> ; <Declaration List>
# <Declaration> ::=  <Qualifier > <IDs>
# <IDs> ::=  <Identifier>    | <Identifier>, <IDs>
# <Statement List> ::=  <Statement>   | <Statement> <Statement List>
# <Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>
# <Compound> ::= {  <Statement List>  }
# <Assign> ::=   <Identifier> := <Expression> ;
# <If> ::= if ( <Condition>  ) <Statement> endif | if ( <Condition>  ) <Statement> else <Statement> endif
# <Return> ::=  return ; |  return <Expression> ;
# <Write> ::=   write ( <Expression>);
# <Read> ::=    read ( <IDs> );
# <While> ::= while ( <Condition>  )  <Statement>
# <Condition> ::= <Expression>  <Relop>   <Expression>

# <Relop> ::=   = |  !=  |   >   | <   |  =>   | <=
def relop():
    if(print_production):
        print('<Relop> ::=   = |  !=  |   >   | <   |  =>   | <=')
    
    if(current.lexeme == '=' or current.lexeme == '!=' or current.lexeme == '>' or 
       current.lexeme == '<' or current.lexeme == '=>' or current.lexeme == '<='):
        getNext()
    else:
        error('= |  !=  |   >   | <   |  =>   | <=') 

# <Expression>  ::= <Expression> + <Term>  | <Expression>  - <Term>  | <Term>
# <Term>    ::=  <Term> * <Factor>  | <Term> / <Factor> |  <Factor>

# <Factor> ::= - <Primary> | <Primary>
def factor():
    if(print_production):
        print('<Factor> ::= - <Primary> | <Primary>')
    
    if(current == '-'):
        getNext()
        primary()
    else:
        primary()

# <Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false
def primary():
    if(print_production):
        print('<Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false')

    if(current.token == 'identifier'):
        getNext()
        #must test if <Identifier> [<IDs>], if no bracket then its just an identifier
        if(current.lexeme == '['):
            getNext()
            ids()
            if(current == ']'): 
                getNext()
            else:
                error(']')
    #    <Integer>
    elif(current.token == 'integer'):
        getNext()
    #    ( <Expression> ) 
    elif(current.lexeme == '('):
        getNext()
        expression()
        if (current.lexeme == ')'):
            getNext()
        else:
            error(')')
    #     <Real>        
    elif(current.token == 'real'):
        getNext()
    #     true
    elif(current.lexeme == 'true'):
        getNext()
    #     false
    elif(current.lexeme == 'false'):
        getNext()
    
    #else does not meet primary requirements
    else:
        error('<Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false')
        
# <Empty> ::= ε
def empty():
    if(print_production):
        print('<Empty> ::= ε')

def error(expected):
    print('\nERROR\nExpected: {}'.format(expected))
    print('Current lexeme: {}'.format(current.lexeme))
    print('Current token: {}'.format(current.token))
    
    #trigger error
    error = False
    
    #pop next and continue
    getNext()

def main():
    tokens = []
    lexemes = []
    
    #call lexer
    tokens, lexemes = Lexer.main()
    #append tokens and lexemes to our global processing deque
    for i in range(len(tokens)):
        lex = Lex(tokens[i], lexemes[i])
        toProcess.append(lex)

#DEBUG
#compares tokens and lexemes together and outputs at user 'quit' if something isnt the same
#     print('printing tokens from deque')
#     for i in range(len(toProcess)):
#         if toProcess[i].token != tokens[i]:
#         print('{}  {}'.format(toProcess[i].token, tokens[i]))
#     print('printing lexemes from deque')
#     for i in range(len(toProcess)):
#         if toProcess[i].lexeme != lexemes[i]:
#         print('{}  {}'.format(toProcess[i].lexeme, lexemes[i]))


if __name__ == '__main__':
    main()