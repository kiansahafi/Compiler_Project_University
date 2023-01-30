""" Parse the given inputs of Mini C language. """

from src.ply_version import parser

from os import listdir, path

EXAMPLE_PATH = './examples/'


def run_parser_examples() -> None:
    """ Run parser on all given examples. """
    example_files = [f for f in listdir(EXAMPLE_PATH)
                     if path.splitext(f)[1] == '.java']

    for example in example_files:
        with open(EXAMPLE_PATH + example, 'r') as file:
            parser.parse_str_ply_version(file.read())
