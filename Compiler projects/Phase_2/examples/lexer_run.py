""" This package run lexer on sample examples. """

from src.ply_version.lexer import PlyLexer

from os import listdir, path

EXAMPLE_PATH = './examples/2.java'


def lex_str_ply_version(input: str) -> None:
    """ Run Ply version of lexer on given input. """
    print('************* Given input *************')
    print(input)
    print('************* Tokens *************')
    lexer = PlyLexer(input)

    for token in lexer.next_token():
        print(token)

    print()


def run_lexer_examples(use_ply: bool = True) -> None:
    """ Run lexer on all given examples. """
    with open(EXAMPLE_PATH, 'r') as file:
        if use_ply:
            lex_str_ply_version(file.read())
