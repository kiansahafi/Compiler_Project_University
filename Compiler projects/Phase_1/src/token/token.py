from enum import Enum


class TokenType(Enum):
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + lexems
    IDENT = "IDENT"
    INT = "INT"
    NUMBER = "NUMBER"
    # Relational Operations :
    RO_LT = "<"
    RO_GT = ">"
    RO_EQ = "=="
    RO_LTE = "<="
    RO_GTE = ">="
    RO_NOT_EQ = "!="

    # Logical operations
    LO_AND = "&&"
    LO_OR = "||"
    LO_NOT = "!"

    # Arithmetic operations
    AO_PLUS = "+"
    AO_MINUS = "-"
    AO_MULTIPLIED = "*"
    AO_DIVISION = "/"

    AO_ASSIGN = "="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    Keyword_TRUE = "true"
    Keyword_FALSE = "false"
    Keyword_IF = "if"
    Keyword_ELSE = "else"
    Keyword_FOR = "for"
    Keyword_WHILE = "while"

    # PrimType
    PrimType_MAIN = "main"
    PrimType_INT = "int"
    PrimType_VOID = "void"
    PrimType_BOOLEAN = "boolean"

    # WhiteSpace
    Space = " "
    Tab = "\t"
    Newline = "\n"
    Returns = "\r"

    # Comment
    StartComment = "/*"
    CloseComment = "*/"
    inlineComment = "//"
    Comment = ""
    # Declarators
    Declarators_public = "public"
    Declarators_private = "private"
    Declarators_static = "static"


KEYWORDS: dict[str, TokenType] = {
    "true": TokenType.Keyword_TRUE,
    "false": TokenType.Keyword_FALSE,
    "if": TokenType.Keyword_IF,
    "else": TokenType.Keyword_ELSE,
    "void": TokenType.PrimType_VOID,
    "boolean": TokenType.PrimType_BOOLEAN,
    "int": TokenType.PrimType_INT,
    "main": TokenType.PrimType_MAIN,
    "for": TokenType.Keyword_FOR,
    "while": TokenType.Keyword_WHILE,
    "public": TokenType.Declarators_public,
    "private": TokenType.Declarators_private,
    "static": TokenType.Declarators_static,

}


class Token:
    type: TokenType
    lexem: str

    def __init__(self, type: TokenType, lexem: str) -> None:
        self.type = type
        self.lexem = lexem

    def __repr__(self) -> str:
        return f'(lexem=" {self.lexem} " -------->    role= [ {self.type} ] )'


def ident_type(ident: str) -> TokenType:
    if ident in KEYWORDS:
        return KEYWORDS[ident]

    return TokenType.IDENT
