import ply.lex as lex
from typing import Generator


class PlyLexer:
    # List of token names.
    tokens = [
        'NUMBER',
        'IDENTIFIER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'EQ',
        'NOT_EQ',
        'LT',
        'GT',
        'LE',
        'GE',
        'LPAREN',
        'RPAREN',
        'ASSIGN',
        'SEMICOLON',
        'LBRACE',
        'RBRACE',
        'COMMA',
        'PLUSASSIGN',
        'AND',
        'NOT',
        'RBRACKET',
        'LBRACKET',

    ]

    # List of reserved words.
    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'int': 'INT',
        'for': 'FOR',
        'char': 'CHAR',
        'do': 'DO',
        'public': 'PUBLIC',
        'private': 'PRIVATE',
        'static': 'STATIC',
        'void': 'VOID',
        'main': 'MAIN',
        'boolean': 'BOOLEAN',
        'return': 'RETURN',
        'true': 'TRUE',
        'false': 'FALSE',
        'this': 'THIS',
        'class': 'CLASS',
        'new': 'NEW'

    }

    tokens = tokens + list(reserved.values())

    t_LE = r'<='
    t_GE = r'>='
    t_EQ = r'=='
    t_PLUSASSIGN = r'\+='
    t_NOT_EQ = r'!='
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ASSIGN = r'='
    t_SEMICOLON = r';'
    t_LBRACE = r'{'
    t_RBRACE = r'}'
    t_LT = r'<'
    t_GT = r'>'
    t_COMMA = r','
    t_AND = r'&&'
    t_NOT = r'!'
    t_RBRACKET = r']'

    # Ignored characters
    t_ignore = ' \t'
    t_ignore_COMMENT = r'\//.*'

    def __init__(self, data: str, **kwargs) -> None:
        """ Initialize lexer. """
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(data)

    # Regular expression for tokenizing numbers
    def t_NUMBER(self, t: lex.LexToken) -> lex.LexToken:
        r'\d+'
        t.value = int(t.value)
        return t

    # def t_eof(self, t: lex.LexToken):
    #     # Get more input (Example)
    #     more = input('... ')
    #     if more:
    #         self.lexer.input(more)
    #         return self.lexer.token()
    #     return None
    # Regular expression for tokenizing identifiers

    def t_IDENTIFIER(self, t: lex.LexToken) -> lex.LexToken:
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        # Check for reserved words
        t.type = self.reserved.get(t.value, 'IDENTIFIER')
        return t

    # Line tracking rule
    def t_newline(self, t: lex.LexToken) -> None:
        r'\n+'
        t.lexer.lineno += len(t.value)

    # Error handling rule
    def t_error(self, t: lex.LexToken) -> None:
        print(f'Illegal character "{t.value[0]}"')
        t.lexer.skip(1)

    def next_token(self):
        for tok in self.lexer:
            print(tok)
