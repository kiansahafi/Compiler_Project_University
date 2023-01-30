from src.lexer.lexer import Lexer
from src.token.token import TokenType
from os import listdir, path

EXAMPLE_PATH = './examples/'


def lex_str(input: str) -> None:
    print('______________ Example ______________')
    print(input)
    print('______________ Lexems + Rules ______________ ')
    lexer = Lexer(input)
    next_token = lexer.next_token()

    while next_token.type != TokenType.EOF:
        print(next_token)
        next_token = lexer.next_token()

    print()




def run_lexer_examples() -> None:
    example_files = [f for f in listdir(EXAMPLE_PATH)
                     if path.splitext(f)[1] == '.java']

    for example in example_files:
        with open(EXAMPLE_PATH + example, 'r') as file:
            lex_str(file.read())
