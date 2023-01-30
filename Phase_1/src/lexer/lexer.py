from ..token.token import Token, TokenType, ident_type


def is_letter(char: str) -> bool:
    return (char >= 'a' and char <= 'z') or \
           (char >= 'A' and char <= 'Z') or char == '_' or (char >= '0' and char <= '9')


def is_char(char: str) -> bool:
    return (char >= 'a' and char <= 'z') or \
           (char >= 'A' and char <= 'Z')


def is_inlinecomment(char: str) -> bool:
    return (char >= 'a' and char <= 'z') or \
           (char >= 'A' and char <= 'Z') or char == ' ' or char == '_' or (char >= '0' and char <= '9')


def is_digit(char: str) -> bool:
    return char >= '0' and char <= '9'


def is_digit_underline(char: str) -> bool:
    return char == '_' or (char >= '0' and char <= '9')


class Lexer:
    input: str
    position: int  # current position in input (points to current char)
    next_position: int  # reading next position in input (after current char)
    current_char: str  # current char under examination

    def __init__(self, input: str) -> None:
        self.input = input
        self.position = 0
        self.next_position = 0
        self.current_char = ''

        self.__read_char()

    def next_token(self) -> Token:
        next_token: Token

        if self.current_char == ';':
            next_token = Token(TokenType.SEMICOLON, self.current_char)
        elif self.current_char == '(':
            next_token = Token(TokenType.LPAREN, self.current_char)
        elif self.current_char == ')':
            next_token = Token(TokenType.RPAREN, self.current_char)
        elif self.current_char == ',':
            next_token = Token(TokenType.COMMA, self.current_char)
        elif self.current_char == '{':
            next_token = Token(TokenType.LBRACE, self.current_char)
        elif self.current_char == '}':
            next_token = Token(TokenType.RBRACE, self.current_char)
        elif self.current_char == '-':
            next_token = Token(TokenType.AO_MINUS, self.current_char)
        elif self.current_char == '+':
            next_token = Token(TokenType.AO_PLUS, self.current_char)


        elif self.current_char == ' ':
            if self.__look_ahead_char() == ' ':
                self.__read_char()
                if self.__look_ahead_char() == ' ':
                    self.__read_char()
                    next_token = Token(TokenType.Tab, "\t")
            else:
                next_token = Token(TokenType.Space, self.current_char)


        elif self.current_char == '\n':

            next_token = Token(TokenType.Newline, "\ n")
        elif self.current_char == '\r':
            next_token = Token(TokenType.Returns, self.current_char)

        elif self.current_char == '/':
            if self.__look_ahead_char() == '/':
                self.__read_char()
                print(f'(lexem=" // "  -------->  type=[ TokenType.StartInlineComment ] )')
                self.__read_char()
                if is_inlinecomment(self.current_char):
                    ident = self.__read_inlinecomment()
                    next_token = Token(TokenType.inlineComment, ident)

            elif self.__look_ahead_char() == '*':
                self.__read_char()
                print(f'( lexem=" /* "  -------->  type=[ TokenType.StartInlineComment ])')
                self.__read_char()
                ident = self.__read_comment()

                next_token = Token(TokenType.Comment, ident)

            else:
                next_token = Token(TokenType.AO_DIVISION, self.current_char)

        elif self.current_char == '*':
            if self.__look_ahead_char() == '/':
                self.__read_char()
                next_token = Token(TokenType.CloseComment, '*/')
            else:
                next_token = Token(TokenType.AO_MULTIPLIED, self.current_char)

        elif self.current_char == 'int':
            next_token = Token(TokenType.PrimType_INT, self.current_char)
        elif self.current_char == 'void':
            next_token = Token(TokenType.PrimType_VOID, self.current_char)
        elif self.current_char == 'boolean':
            next_token = Token(TokenType.PrimType_BOOLEAN, self.current_char)


        elif self.current_char == '<':
            if self.__look_ahead_char() == '=':
                self.__read_char()
                next_token = Token(TokenType.RO_LTE, '<=')
            else:
                next_token = Token(TokenType.RO_LT, self.current_char)

        elif self.current_char == '>':
            if self.__look_ahead_char() == '=':
                self.__read_char()
                next_token = Token(TokenType.RO_GTE, '>=')
            else:
                next_token = Token(TokenType.RO_GT, self.current_char)

        elif self.current_char == '':
            next_token = Token(TokenType.EOF, self.current_char)
        elif self.current_char == '=':
            if self.__look_ahead_char() == '=':
                self.__read_char()
                next_token = Token(TokenType.RO_EQ, '==')
            else:
                next_token = Token(TokenType.AO_ASSIGN, self.current_char)

        elif self.current_char == '!':
            if self.__look_ahead_char() == '=':
                self.__read_char()
                next_token = Token(TokenType.RO_NOT_EQ, '!=')
            else:
                next_token = Token(TokenType.LO_NOT, self.current_char)
        elif self.current_char == '&':
            if self.__look_ahead_char() == '&':
                self.__read_char()
                next_token = Token(TokenType.LO_AND, '&&')
        elif self.current_char == '|':
            if self.__look_ahead_char() == '|':
                self.__read_char()
            next_token = Token(TokenType.LO_OR, '||')

        elif is_digit_underline(self.current_char):
            if (is_char(self.__look_ahead_char())):
                illegal = self.__read_illegal()
                next_token = Token(TokenType.ILLEGAL, illegal)
                return next_token
            else:
                if (is_digit(self.current_char)):
                    number = self.__read_digit()
                    next_token = Token(TokenType.NUMBER, number)
                    return next_token

        else:

            if is_letter(self.current_char):
                ident = self.__read_identifier()
                next_token = Token(ident_type(ident), ident)
                return next_token
            else:
                next_token = Token(TokenType.ILLEGAL, self.current_char)

        self.__read_char()
        return next_token

    def __read_char(self) -> None:
        if self.next_position >= len(self.input):
            self.current_char = ''
        else:
            self.current_char = self.input[self.next_position]

        self.position = self.next_position
        self.next_position += 1

    def __look_ahead_char(self) -> str:
        if self.next_position >= len(self.input):
            return ''
        else:
            return self.input[self.next_position]

    def __look_ahead_2char(self) -> str:
        if self.next_position >= len(self.input):
            return ''
        else:
            return self.input[self.next_position + 1]

    def __read_illegal(self) -> str:
        position = self.position
        while is_letter(self.current_char):
            self.__read_char()
        return self.input[position:self.position]

    def __read_identifier(self) -> str:
        position = self.position
        while is_letter(self.current_char):
            self.__read_char()

        return self.input[position:self.position]

    def __read_digit(self) -> str:
        position = self.position
        while is_digit(self.current_char):
            self.__read_char()

        return self.input[position:self.position]

    def __read_inlinecomment(self) -> str:
        position = self.position
        while (self.current_char != "\n"):
            self.__read_char()
        return self.input[position:self.position]

    def __read_comment(self) -> str:
        position = self.position
        while ((self.__look_ahead_char() != "*/" and self.__look_ahead_2char() != "/")):
            self.__read_char()

        return self.input[position:self.position]

    def __read_number(self) -> str:
        position = self.position

        while is_digit(self.current_char):
            self.__read_char()

        return self.input[position:self.position]
