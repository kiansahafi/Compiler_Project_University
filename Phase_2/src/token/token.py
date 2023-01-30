""" Main package of token class and it's helper functions. """
from enum import Enum


class TokenType(Enum):
    """ Define TokenType enums. """

    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1343456

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"
    LT = "<"
    GT = ">"
    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    INT_KW = "INT_KW"
    CHAR_KW = "CHAR_KW"
    FLOAT_KW = "FLOAT_KW"
    FOR = "FOR"
    WHILE = "WHILE"


# Map a string to it's related TokenType
KEYWORDS: dict[str, TokenType] = {
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "char": TokenType.CHAR_KW,
    "float": TokenType.FLOAT_KW,
    "int": TokenType.INT_KW,
    "for": TokenType.FOR,
    "while": TokenType.WHILE,
}


class Token:
    """ Main token class. """

    type: TokenType
    literal: str

    def __init__(self, type: TokenType, literal: str) -> None:
        self.type = type
        self.literal = literal

    def __repr__(self) -> str:
        return f'Token<type="{self.type}", literal="{self.literal}">'


def lookup_ident_type(ident: str) -> TokenType:
    """ Return TokenType of a identifier. """
    if ident in KEYWORDS:
        return KEYWORDS[ident]

    return TokenType.IDENT
