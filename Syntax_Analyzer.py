#Art Grichine
#Zeed Jarrah
#ArtGrichine@csu.fullerton.edu
#ZJarrah@csu.fullerton.edu
#Syntax Analyser (Assignment 2)
#Requires Python version > 2.5 because of use of ternary operations

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
_print = True            #toggles print feature for the SA production
toProcess = deque()
current = Lex()
error = True
peek_next = Lex()


#when an error is found, the expected variable is sent here and error is reported
def error(expected):
    print('\nERROR\nExpected: {}'.format(expected))
    print('Current lexeme: {}'.format(current.lexeme))
    print('Current token: {}'.format(current.token))
    
    #trigger error
    error = False
    
    sys.exit()      #exit program
    
    #pop next and continue
    # getNext()
    
#set current to the next variable to process
def getNext():
    global current                          #access the current global variable

    if toProcess:                           #if not empty
        current = toProcess.popleft()
        printInfo()

#used to peek at the next variable in toProcess
def peek():
    global peek_next                        #access the peek_next global variable
    if toProcess:
        peek_next = toProcess[0]

def printInfo():
    if current.token:
        if _print:
            print('Token: {0:14} Lexeme: {1:1}'.format(current.token, current.lexeme))
    else:
        print('ERROR: current is empty')
    
####  Production Rules  ####
#<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> 
def rat15S():
    #initial production
    if _print:
        print('<Rat15S>  ::=   <Opt Function Definitions>  @@  <Opt Declaration List> @@  <Statement List> ')
    
    optFunctionDefinitions()
    getNext()
    
    if current.lexeme == '@@':
        getNext()
        optDeclarationList()
        
        if current.lexeme == '@@':
            getNext()
            statmentList()
        
        else:
            error('@@')
        
    else:
        error('@@')

#<Opt Function Definitions> ::= <Function Definitions> | <Empty>
def optFunctionDefinitions():
    if _print:
        print('<Opt Function Definitions> ::= <Function Definitions> | <Empty>') 
    
    if current.lexeme == 'function':
        functionDefinitions()
    elif current.token == 'unknown':
        error('<Function Definitions> | <Empty>')
    else:
        empty()   

#<Function Definitions>  ::= <Function> | <Function> <Function Definitions>   
def functionDefinitions():
    if _print:
        print('<Function Definitions> ::= <Function> | <Function> <Function Definitions>')
    
    #continue gathering function definitions until there are no more to report
    while(True):
        function()
        if current.lexeme != 'function':
            break

#<Function> ::= function  <Identifier> [ <Opt Parameter List> ]   <Opt Declaration List>  <Body>
def function():
    if _print:
        print('<Function> ::= function  <Identifier> [ <Opt Parameter List> ]   <Opt Declaration List>  <Body>')
    
    #function
    if current.lexeme == 'function':
        getNext()
    
        #<Identifier>
        if current.token == 'identifier':
            getNext()
            
            # [
            if current.lexeme == '[':
                getNext()
            
                #<Opt Parameter List>
                if current.token == 'identifier':
                    getNext()
                
                    if current.lexeme == ']':
                        getNext()
                        optDeclarationList
                        body()
                    
                    else:
                        error(']')
                
                else:
                    error('<Opt Parameter List>')
            
            else:
                error('[')
        
        else:
            error('<Identifier>')
    
    else:
        error('function')

# <Opt Parameter List> ::=  <Parameter List>   |  <Empty>
def optParameterList():
    if _print:
        print('<Opt Parameter List> ::=  <Parameter List> | <Empty>')
    
    if current.token == 'identifier':
        parameterList()
    elif current.token == 'unknown':
        error('<Parameter List> | <Empty>')
    else:
        empty()

# <Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>
def parameterList():
    if _print:
        print('<Parameter List> ::= <Parameter> | <Parameter> , <Parameter List>')
    
    parameter()
    getNext()
    
    if current.lexeme == ',':
        parameterList()

# <Parameter> ::=  < IDs > : <Qualifier>
def parameter():
    if _print:
        print('<Parameter> ::=  < IDs > : <Qualifier>')
    
    if current.token == 'identifier':
        ids()
        getNext()
        
        if current.lexeme == ':':
            getNext()
            qualifier()
        
        else:
            error('<Qualifier>')
        
    else:
        error('< IDs >')


# <Qualifier> ::= int | boolean | real
def qualifier():
    if _print:
        print('<Qualifier> ::= int | boolean | real')
    
    if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
        getNext()
    else:
        error('int | boolean | real')

# <Body>  ::=  {  < Statement List>  }
def body():
    if _print:
        print('<Body>  ::=  {  < Statement List>  }')
    
    if current.lexeme == '{':
        getNext()
        statementList()
        
        getNext() if current.lexeme == '}' else error('}')
    
    else:
        error('{')

# <Opt Declaration List> ::= <Declaration List> | <Empty>
def optDeclarationList():
    if _print:
        print('<Opt Declaration List> ::= <Declaration List> | <Empty>')
    
    #check for qualifier
    if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
        declarationList()
    elif current.token == 'unknown':
        error('<<Declaration List> | <Empty>')
    else:
        empty()

# <Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>
def declarationList():
    if _print:
        print('<Declaration List> := <Declaration> ; | <Declaration> ; <Declaration List>')
    
    declaration()
    getNext()
    
    if current.lexeme == ';':
        getNext()
        #see if the next is a qualifier --> int, boolean, real
        if current.lexeme == 'int' or current.lexeme == 'boolean' or current.lexeme == 'real':
            declarationList()
    else:
        error(';')
    
    # peek()
    #
    # while(True):
    #     #see if the next is a qualifier --> int, boolean, real
    #     if current.lexeme == ';' and any(peek_next.lexeme == 'int' or peek_next.lexeme == 'boolean' or peek_next.lexeme == 'real'):
    #         getNext()
    #         declaration()
    #     elif current.lexeme == ';':
    #         getNext()
    #         break
    #     else:
    #         error(';')
    #         break
    #

    


# <Declaration> ::=  <Qualifier > <IDs>
def declaration():
    if _print:
        print('<Declaration> ::= <Qualifier > <IDs>')
    
    qualifier()
    ids()


# <IDs> ::=  <Identifier> | <Identifier>, <IDs>
def ids():
    if _print:
        print('<IDs> ::=  <Identifier> | <Identifier>, <IDs>')
    
    peek()
    
    # <Identifier> 
    if current.token != 'identifier':
        error('<Identifier>')
    elif current.token == 'identifier' and peek_next.lexeme != ',':
        getNext()
    else:
        # <Identifier>, <IDs>
        while True:
            if current.token == 'identifier' and peek_next.lexeme == ',':
                getNext()
            elif current.token == 'identifier' and peek_next.lexeme != ',':
                getNext()
                break
            else:
                error('<Identifier>, <IDs>')

# <Statement List> ::= <Statement> | <Statement> <Statement List>
def statementList():
    if _print:
        print('<Statement List> ::= <Statement> | <Statement> <Statement List>')
    
    while True:
        valid = statement()
        #must test to see if possible statement. Will test for compound, assign, if, return, write,
        #  read, while. If there is another statement then continue loop, otherwise break
        if current.lexeme != '{' or current.token != 'identifier' or current.lexeme != 'if' or current.lexeme != 'return' or current.lexeme != 'write' or current.lexeme != 'read' or current.lexeme != 'while':
            break

# <Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>
def statement():
    if _print:
        print('<Statement> ::=  <Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>')
    
    #compound starts with '{' so we test for compound by looking for '{' lexeme in current
    if current.lexeme == '{':
        compound()
    #assign starts with an identifier, test for assign by checking if 'identifier' token in current
    elif current.token == 'identifier':
        assign()
    #if operations all start with 'if', check current lexeme for 'if'
    elif current.lexeme == 'if':
        _if()
    #return operators start with return, check current lexeme for 'return'
    elif current.lexeme == 'return':
        _return()
    #write begins with write, check current lexeme for 'write'
    elif current.lexeme == 'write':
        write()
    #read begins with read, check current lexeme for 'read'
    elif current.lexeme == 'read':
        read()
    #while begins with while, check current lexeme for 'while'
    elif current.lexeme == 'while':
        _while()
    else:
        error('<Compound> | <Assign> | <If> |  <Return> | <Write> | <Read> | <While>')

# <Compound> ::= {  <Statement List>  }
def compound():
    if _print:
        print('<Compound> ::= {  <Statement List>  }')
    
    if current.lexeme == '{':
        getNext()
        statementList()
        
        getNext() if current.lexeme == '}' else error('}')
        
        
    else:
        error('{')

# <Assign> ::=   <Identifier> := <Expression> ;
def assign():
    if _print:
        print('<Assign> ::=   <Identifier> := <Expression> ;')
    
    if current.token == 'identifier':
        getNext()
    
        if current.lexeme == ':=':
            getNext()
            expression()
        
            getNext() if current.lexeme == ';' else error(';')
                
        else:
            error(':=')
    
    else:
        error('<Identifier>')

# <If> ::= if ( <Condition>  ) <Statement> endif | if ( <Condition>  ) <Statement> else <Statement> endif
# <Return> ::=  return ; |  return <Expression> ;
def _return():
    if _print:
        print('<Return> ::=  return ; |  return <Expression> ;')
    
    peek()
    
    #condition 1:   return ;  
    if peek_next.lexeme == ';':
        
        if current.lexeme == 'return':
            getNext()   
        
            if current.lexeme == ';':
                getNext()
            else:
                error(';')
        
        else:
            error('return')
    
    #condition 2:   return <Expression> ;
    else:
        if current.lexeme == 'return':
            getNext()
            expression()
            
            getNext() if current.lexeme == ';' else error(';')
            
        else:
            error('return')
        

# <Write> ::=   write ( <Expression>);
def write():
    if _print:
        print('<Write> ::=   write ( <Expression>);')
    
    if current.lexeme == 'write':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            expression()
        
            if current.lexeme == ')':
                getNext()
                    
                getNext() if current.lexeme == ';' else error(';')
                
            else:
                error(')')
        
        else:
            error('<Expression>')
    
    else:
        error('write')

# <Read> ::= read ( <IDs> );
def read():
    if _print:
        print('<Read> ::= read ( <IDs> );')
    
    if current.lexeme == 'read':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            ids()
            
            if current.lexeme == ')':
                getNext()
                
                getNext() if current.lexeme == ';' else error(';')
                
            else:
                error(')')
            
        else:
            error('(')
    
    else:
        error('read')

# <While> ::= while ( <Condition>  )  <Statement>
def _while():
    if _print:
        print('<While> ::= while ( <Condition>  )  <Statement>')
    
    if current.lexeme == 'while':
        getNext()
        
        if current.lexeme == '(':
            getNext()
            condition()
            
            if current.lexeme == ')':
                getNext()
                statement()
            else:
                error(')')
        
        else:
            error('(')
        
    else:
        error('while')

# <Condition> ::= <Expression> <Relop> <Expression>
def condition():
    if _print:
        print('<Condition> ::= <Expression> <Relop> <Expression>')
    
    expression()
    relop()
    expression()

# <Relop> ::=   = |  !=  |   >   | <   |  =>   | <=
def relop():
    if _print:
        print('<Relop> ::=   = |  !=  |   >   | <   |  =>   | <=')
    
    if current.lexeme == '=' or current.lexeme == '!=' or current.lexeme == '>' or current.lexeme == '<' or current.lexeme == '=>' or current.lexeme == '<=':
        getNext()
    else:
        error('= |  !=  |   >   | <   |  =>   | <=') 

# <Expression> ::= <Term> <ExpressionPrime>
def expression():
    if _print:
        print('<Expression> ::= <Term> <ExpressionPrime>')
    
    term()
    expressionPrime()

# <ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <empty>
def expressionPrime():
    if _print:
        print('<ExpressionPrime> ::= + <Term> <ExpressionPrime> | - <Term> <ExpressionPrime> | <empty>')
    
    if current.lexeme == '+' or current.lexeme == '-':
        getNext()
        term()
        expressionPrime()
    elif current.token == 'unknown':
        error('+, -, <empty>')    
    else:
        empty()


# <Term> ::= <Factor> <TermPrime>
def term():
    if _print:
        print('<Term> ::= <Factor> <TermPrime>')
    
    factor()
    termPrime()

# <TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <empty>
def termPrime():
    if _print:
        print('<TermPrime> ::= * <Factor> <TermPrime> | / <Factor> <TermPrime> | <empty>')
    
    if current.lexeme == '*' or current.lexeme == '/':
        getNext()
        factor()
        termPrime()
    elif current.token == 'unknown':
        error('*, /, <empty>')    
    else:
        empty()    



# <Factor> ::= - <Primary> | <Primary>
def factor():
    if _print:
        print('<Factor> ::= - <Primary> | <Primary>')
    
    if current == '-':
        getNext()
        primary()
    else:
        primary()
        
# <Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false
def primary():
    if _print:
        print('<Primary> ::= <Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false')

    if current.token == 'identifier':
        getNext()
        #must test if <Identifier> [<IDs>], if no bracket then its just an identifier
        if current.lexeme == '[':
            getNext()
            ids()
            getNext() if current == ']' else error(']')

    #    <Integer>
    elif current.token == 'integer':
        getNext()
    #    ( <Expression> ) 
    elif current.lexeme == '(':
        getNext()
        expression()
        getNext() if current.lexeme == ')' else error(')')

    #     <Real>        
    elif current.token == 'real':
        getNext()
    #     true
    elif current.lexeme == 'true':
        getNext()
    #     false
    elif current.lexeme == 'false':
        getNext()
    
    #else does not meet primary requirements
    else:
        error('<Identifier> | <Integer> | <Identifier> [<IDs>] | ( <Expression> ) |  <Real>  | true | false')
        
# <Empty> ::= ε
def empty():
    if _print:
        print('<Empty> ::= ε')


#purpose: Drive Syntax Analyser
def main():
    tokens = []
    lexemes = []
    
    #call lexer
    tokens, lexemes = Lexer.main()
    #append tokens and lexemes to our global processing deque
    for i in range(len(tokens)):
        lex = Lex(tokens[i], lexemes[i])
        toProcess.append(lex)
    
    
    getNext()       #get first input
    while toProcess:
        rat15S()

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