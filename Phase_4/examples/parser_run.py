from src.ply_version import parser

EXAMPLE_PATH = './examples/3.java'


def run_parser_examples() -> None:
    with open(EXAMPLE_PATH, 'r') as file:
        parser.parse_str_ply_version(file.read())
