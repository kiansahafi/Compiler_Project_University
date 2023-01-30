""" This package run lexer on sample examples. """

from src.ply_version.lexer import PlyLexer

from os import listdir, path

EXAMPLE_PATH = './examples/'


def lex_str_ply_version(input: str):
    """ Run Ply version of lexer on given input. """
    print('************* Given input *************')
    print(input)
    print('************* Tokens *************')

    lexer = PlyLexer(input)

    for token in lexer.next_token():
        print(token)

    print()


def run_lexer_examples(use_ply: bool = True):
    """ Run lexer on all given examples. """
    example_files = [f for f in listdir(EXAMPLE_PATH)
                     if path.splitext(f)[1] == '.java']

    for example in example_files:
        with open(EXAMPLE_PATH + example, 'r') as file:
            if use_ply:
                lex_str_ply_version(file.read())
