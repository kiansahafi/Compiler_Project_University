from ply.yacc import YaccProduction
from src.ply_version.lexer import PlyLexer

tokens = PlyLexer.tokens


def p_s(p: YaccProduction):
    '''start : ClassDeclaration
            | empty
            | exp
            '''
    p[0] = p[1]


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
    | VOID
    | FLOAT
    '''
    p[0] = p[1]
    pass


def p_classtype(p: YaccProduction):
    '''ClassType : IDENTIFIER  '''
    p[0] = p[1]
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
    p[0] = p[1]
    pass


def p_statement(p: YaccProduction):
    '''statement : empty
                | if_st
                | while_st
                | LBRACE statement RBRACE
                | Refrence LPAREN argumentlist RPAREN
                | Refrence LPAREN RPAREN SEMICOLON
                | Refrence LBRACKET exp RBRACKET ASSIGN exp SEMICOLON
                | Refrence ASSIGN exp SEMICOLON
                | PrimeType IDENTIFIER ASSIGN IDENTIFIER SEMICOLON
                | PrimeType IDENTIFIER ASSIGN exp SEMICOLON
                | statement statement
                | exp'''

    if len(p) == 6:
        if (str(p.slice[1].value) == 'int'):
            if str(p.slice[4].value) == ",":
                print(f"INT Variable Can not Initialize With Float Value In Line : {p.slice[3].lineno} ")
                quit()

    if (str(p.slice[1].value) == 'int'):
        if ((str(p.slice[4].value) != ",") and str(type(p.slice[4].value)) == "<class 'str'>"):
            print(f"Int Variable Can not Initialize With String Value In Line : {p.slice[3].lineno} ")
            quit()

    if (str(p.slice[1].value) == 'float'):
        if str(type(p.slice[4].value)) == "<class 'str'>":
            print(f"Float Variable Can not Initialize With String Value In Line : {p.slice[3].lineno} ")
            quit()

    pass


def p_while_st(p: YaccProduction):
    '''while_st : WHILE LPAREN exp RPAREN statement'''
    pass


def p_if_st(p: YaccProduction):
    '''if_st : IF LPAREN exp RPAREN statement ELSE statement
    | IF LPAREN exp RPAREN statement '''
    pass


def p_exp(p: YaccProduction):
    '''exp :
    | exp Binop exp
    | IDENTIFIER
    | Type exp
    | Refrence LBRACKET exp RBRACKET
    | Refrence LPAREN RPAREN
    | Refrence LPAREN argumentlist RPAREN
    | Unop exp
    | LPAREN exp RPAREN
    | TRUE
    | IDENTIFIER Binop NUMBER
    | FALSE
    | NEW IDENTIFIER LPAREN RPAREN
    | NEW INT LBRACKET exp RBRACKET
    | NEW IDENTIFIER LBRACKET exp RBRACKET
    | NUMBER Binop NUMBER
    | NUMBER Binop float
    | float Binop NUMBER
    | float Binop float

    '''
    if (len(p) == 4) and (str(p.slice[3].type) == 'float'):
        p[0] = p[3]
    if (len(p) == 4) and (str(p.slice[1].type) == 'float'):
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_Unop(p: YaccProduction):
    ''' Unop : NOT
    | MINUS'''

    p[0] = p[1]
    pass


def p_float(p: YaccProduction):
    ''' float : NUMBER COMMA NUMBER '''
    p[0] = p[2]
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

    p[0] = p[1]

    pass


def p_empty(p: YaccProduction):
    'empty : '
    pass


def p_error(p: YaccProduction):
    token = f"'{p.value}' on line {p.lineno}"

    raise Exception(f'Syntax error : {token}')


import ply.yacc as yacc

parser = yacc.yacc(method='LALR', debug=True)


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

    print("\n\n\n")
