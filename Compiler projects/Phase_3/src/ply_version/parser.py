import ply.yacc as yacc
from ply.yacc import YaccProduction
from ply import lex, yacc
from src.ply_version.lexer import PlyLexer

tokens = PlyLexer.tokens


def p_s(p: YaccProduction):
    '''start : ClassDeclaration
            | empty
            | exp
            | ClassDeclaration ClassDeclaration '''
    pass


def p_ClassDeclaration(p: YaccProduction):
    '''ClassDeclaration : CLASS IDENTIFIER LBRACE RBRACE
            | CLASS IDENTIFIER LBRACE MethodDeclaration RBRACE
            | CLASS IDENTIFIER LBRACE FieldDeclaration RBRACE'''

    pass


def p_FieldDeclaration(p: YaccProduction):
    '''FieldDeclaration : Declarators IDENTIFIER SEMICOLON'''
    pass


def p_MethodDeclaration(p: YaccProduction):
    '''MethodDeclaration : Declarators IDENTIFIER LPAREN RPAREN LBRACE statement RBRACE
    | Declarators IDENTIFIER LPAREN RPAREN LBRACE statement RETURN exp SEMICOLON RBRACE
    | Declarators IDENTIFIER LPAREN ParameterList RPAREN LBRACE statement RETURN exp SEMICOLON RBRACE
    | Declarators IDENTIFIER LPAREN ParameterList RPAREN LBRACE statement RBRACE '''
    pass


def p_ParameterList(p: YaccProduction):
    '''ParameterList : Type IDENTIFIER
    | Type IDENTIFIER COMMA Type IDENTIFIER'''
    pass


def p_Declarators(p: YaccProduction):
    '''Declarators : Type
    | STATIC Type
    | PUBLIC Type
    | PRIVATE Type
    | PUBLIC STATIC Type
    | PRIVATE STATIC Type'''
    pass


def p_type(p: YaccProduction):
    '''Type : PrimeType
    | ClassType
    | arraytype '''
    pass


def p_primtype(p: YaccProduction):
    '''PrimeType : INT
    | BOOLEAN
    | VOID '''
    pass


def p_classtype(p: YaccProduction):
    '''ClassType : IDENTIFIER  '''

    pass


def p_arraytype(p: YaccProduction):
    '''arraytype : INT LBRACKET RBRACKET
    | ClassType LBRACKET RBRACKET  '''
    pass


def p_argumentlist(p: YaccProduction):
    '''argumentlist : exp
    | exp COMMA exp '''
    pass


def p_refrence(p: YaccProduction):
    '''Refrence : THIS
    | IDENTIFIER '''
    pass


def p_statement(p: YaccProduction):
    '''statement : if_st
                | while_st
                | LBRACE statement RBRACE
                | Refrence LPAREN argumentlist RPAREN SEMICOLON
                | Refrence LPAREN RPAREN SEMICOLON
                | Refrence LBRACKET exp RBRACKET ASSIGN exp SEMICOLON
                | Refrence ASSIGN exp SEMICOLON
                | Type IDENTIFIER ASSIGN exp SEMICOLON
                | empty
                | statement statement '''

    pass


def p_while_st(p: YaccProduction):
    '''while_st : WHILE LPAREN exp RPAREN statement'''
    pass


def p_if_st(p: YaccProduction):
    '''if_st : IF LPAREN exp RPAREN statement
    | IF LPAREN exp RPAREN statement ELSE statement'''
    pass


def p_exp(p: YaccProduction):
    '''exp : Refrence
    | Type exp
    | Refrence LBRACKET exp RBRACKET
    | Refrence LPAREN RPAREN
    | Refrence LPAREN argumentlist RPAREN
    | Unop exp
    | exp Binop exp
    | LPAREN exp RPAREN
    | NUMBER
    | TRUE
    | IDENTIFIER Binop NUMBER
    | FALSE
    | NEW IDENTIFIER LPAREN RPAREN
    | NEW INT LBRACKET exp RBRACKET
    | NEW IDENTIFIER LBRACKET exp RBRACKET
    '''
    pass


def p_Unop(p: YaccProduction):
    ''' Unop : NOT
    | MINUS'''
    pass


def p_Binop(p: YaccProduction):
    '''Binop : PLUS
    | MINUS
    | TIMES
    | DIVIDE
    | EQ
    | NOT_EQ
    | LT
    | GT
    | LE
    | GE
    | AND
    | NOT
    '''
    pass


def p_empty(p: YaccProduction):
    'empty : '
    pass


def p_error(p: YaccProduction):
    token = f"'Last Token Before {p.value}' on line {p.lineno}"

    raise Exception(f'Syntax error : {token}')

    pass


import ply.yacc as yacc

parser = yacc.yacc()


def parse_str_ply_version(input: str) -> None:
    """ Run Ply version of parser on given input. """
    print('************* Given input *************')
    print(input)
    print('************* Result *************')

    lexer = PlyLexer(input)
    try:
        result = parser.parse(input)
    except Exception as e:
        print(e)
    else:
        print("Compiled SuccessFully")

    print('\n\n\n')
