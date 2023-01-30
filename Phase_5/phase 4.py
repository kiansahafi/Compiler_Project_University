import ply.yacc as yacc
import ply.lex as lex

tokens = [
    'IDENTIFIER', 'INTEGER', 'CHARACTER', 'FLOAT', 'STRING',
    'OP_add', 'OP_subtract', 'OP_multiply', 'OP_divide', 'OP_negate', 'OP_mod', 'OP_assign',
    'OP_greater', 'OP_less', 'OP_greaterequal', 'OP_lessequal', 'OP_equal', 'OP_notequal',

    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'SEMICOLON', 'COMMA',
    'KEY_if', 'KEY_else', 'KEY_do', 'KEY_while', 'KEY_for',
    'KEY_int', 'KEY_char', 'KEY_float', 'KEY_string',
    'KEY_print'
]

# Tokens
t_OP_add = r'\+'
t_OP_subtract = r'-'
t_OP_multiply = r'\*'
t_OP_divide = r'/'
t_OP_mod = r'%'
t_OP_assign = r'='
t_OP_greater = r'>'
t_OP_less = r'<'
t_OP_greaterequal = r'>='
t_OP_lessequal = r'<='
t_OP_equal = r'=='
t_OP_notequal = r'!='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COMMA = r','

reserved = {
    'if': 'KEY_if',
    'else': 'KEY_else',
    'do': 'KEY_do',
    'while': 'KEY_while',
    'for': 'KEY_for',
    'int': 'KEY_int',
    'char': 'KEY_char',
    'float': 'KEY_float',
    'string': 'KEY_string',
    'print': 'KEY_print',
    'scan': 'KEY_scan',
}


def get_key_from_value(d, val):
    for key, value in d.items():
        if val == value:
            return key


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_FLOAT(t):
    r'(\d*)?\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_CHARACTER(t):
    r"'([^'\n]|\\n|\\\\)'"
    t.value = t.value[1]
    return t


def t_STRING(t):
    r"\"([^'\n]|\\n|\\\\)*\""
    t.value = t.value[1:-1]
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(t.lexer.lexdata)
    print(" " * t.lexer.lexpos, end="")
    print('^ ')
    print(f"Illegal character {t.value[0]!r}")
    t.lexer.skip(1)


l = lex.lex()
precedence = (('right', 'OP_negate'),)

memory_address = []
name = []
temp_name = []
ss = []

loop = []  # Bara Shenasayi Avalin Khat Dar For && If && While ....
endloop = []  # Bara Shenasayi Akharin Khat Dar For && If && While ....

output_code = []
main_memory_pointer = 100
temp_memory_pointer = 500
diction = {}
diction_value = {}
number = []

start = 'statement_list'


def p_statement(p):
    '''statement : compound_statement
                 | declaration_statement
                 | selection_statement
                 | iteration_statement
                 | expression_statement
                 | SEMICOLON'''
    p[0] = p[1]


def p_compound_statement(p):  ##
    'compound_statement : LBRACE statement_list RBRACE end'
    p[0] = p[2]
    end = p.slice[3].lineno
    endloop.append(end)


def p_statement_list(p):  ##
    '''statement_list : statement_list statement
                      | empty'''


def p_declaration_statement(p):
    'declaration_statement : type_specifier declaration_list SEMICOLON'


def p_type_specifier(p):
    '''type_specifier : KEY_int
                      | KEY_char
                      | KEY_float
                      | KEY_string
    '''
    p[0] = p[1]


def p_declaration_list(p):
    '''declaration_list : single_var_declation COMMA declaration_list
                        | single_var_declation
    '''


def p_single_var_declation(p):
    '''single_var_declation : IDENTIFIER
                            | IDENTIFIER OP_assign primary_expression
    '''
    global main_memory_pointer

    if not (p[1] in name):
        name.append(p[1])
        diction.update({p[1]: main_memory_pointer})  # Ekhtesas Dadan Yek Khane Az Memory Be Variableha
        main_memory_pointer = main_memory_pointer + 1

    if ((p[1] in name) and (len(temp_name) > 1)):
        output_code.append(
            f':=, {diction_value.get(temp_name[len(temp_name) - 2])} ,M({diction.get(temp_name.pop(-2))}) ')

    if len(p) > 2:
        diction_value.update({p[1]: p[3]})  # Ezafe Kardan Value Be Variable Marbute

    temp_name.append(p[1])  # Ezafe shodan Variable Dakhel Stack

    print(f"append {temp_name}")


def p_selection_statement(p):
    '''selection_statement : KEY_if LPAREN expression save RPAREN statement
                           | KEY_if LPAREN expression save RPAREN statement KEY_else save statement'''
    global temp_memory_pointer
    if len(p) < 8:  # IF

        index = ss.pop()
        if ((temp_memory_pointer - 2) > 499):
            output_code[index] = f'JPF, M({temp_memory_pointer - 2}) ,{endloop.pop()} , '  # Jump Out From If False




    else:  # IF ELSE
        index = ss.pop()
        output_code[index] = f'JP, {endloop.pop()}, , '  # Jump Out From Else
        index2 = ss.pop()
    if ((temp_memory_pointer - 2) > 499):
        output_code[index2] = f'JPF, M({temp_memory_pointer - 1}),{p.slice[7].lineno} '  # Jump to Else


def p_iteration_statement(p):
    '''iteration_statement : KEY_while label LPAREN expression save RPAREN statement end
                           | KEY_for LPAREN optexpr label SEMICOLON optexpr save SEMICOLON optexpr RPAREN statement'''

    if p[1] == 'while':
        lineno = p.slice[1].lineno
        loop.append(lineno)
        index = ss.pop()
        if ((temp_memory_pointer - 3) > 99):
            output_code[index] = f'JPF, M({main_memory_pointer - 1}) , {endloop.pop()}, '  # Jump Out From While
            output_code.append(f'JP, {loop.pop()}, , ')
        else:
            output_code[index] = f'JPF, M({main_memory_pointer}) , {endloop.pop()}, '  # Jump Out From While
            output_code.append(f'JP, {loop.pop()}, , ')  # Jump to While

    if p[1] == 'for':
        index = ss.pop()

        lineno = p.slice[1].lineno
        loop.append(lineno)
        if ((temp_memory_pointer - 3) > 500):
            output_code[index] = f'JPF, M({temp_memory_pointer - 3}) , {endloop.pop()}, '  # Jump out From For
            output_code.append(f'JP, {loop.pop()}, , ')  # Jump to For
        else:
            output_code[index] = f'JPF, M({temp_memory_pointer - 3}) , {endloop.pop()}, '  # Jump out From For
            output_code.append(f'JP, {loop.pop()}, , ')  # Jump to For


def p_label(p):
    'label : empty'
    ss.append(len(output_code))


def p_save(p):
    'save : empty'
    ss.append(len(output_code))
    output_code.append(f'save')


def p_end(p):
    'end : empty'


def p_optexpr(p):
    '''optexpr : assignment_expression
               | empty
    '''


def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'


def p_expression(p):
    '''expression : assignment_expression
                  | expression COMMA assignment_expression
    '''
    if len(p) < 3:
        p[0] = p[1]


def p_assignment_expression(p):
    '''assignment_expression : IDENTIFIER OP_assign primary_expression
                            | primary_expression
                            | OP_subtract primary_expression %prec OP_negate
                            | primary_expression OP_multiply primary_expression
                            | primary_expression OP_divide primary_expression
                            | primary_expression OP_mod primary_expression
                            | primary_expression OP_add primary_expression
                            | primary_expression OP_subtract primary_expression
                            | primary_expression OP_greater primary_expression
                            | primary_expression OP_less primary_expression
                            | primary_expression OP_greaterequal primary_expression
                            | primary_expression OP_lessequal primary_expression
                            | primary_expression OP_equal primary_expression
                            | primary_expression OP_notequal primary_expression
                            | IDENTIFIER OP_assign assignment_expression



    '''

    global temp_memory_pointer
    if len(p) > 2:
        print(f"{str(p.slice[1].type)} {str(p.slice[2].type)} {str(p.slice[3].type)}")

        if (str(p.slice[1].type) == "IDENTIFIER" and str(p.slice[2].type) == "OP_assign" and str(
                p.slice[3].type) == "primary_expression"):
            if len(p) > 2:
                diction_value.update({p[1]: p[3]})

                if (len(temp_name) > 2):
                    print(f"p : {p[1]}{p[2]}{p[3]}")
                    print(f"Temp Name : {temp_name}")
                    print(f"Dictionary Value : : {diction_value}")
                    output_code.append(
                        f':=, {temp_name[len(temp_name) - 1]} ,M({temp_name.pop()}) ')  # Assign Value Be Direct Memory Address

                else:

                    output_code.append(
                        f':=, {diction_value.get(temp_name[len(temp_name) - 1])} ,M({diction.get(temp_name.pop())}) ')

        if (str(p.slice[1].type) == "IDENTIFIER" and str(p.slice[2].type) == "OP_assign" and str(
                p.slice[3].type) == "assignment_expression"):
            print(temp_name)
            output_code.append(
                f':=, M({temp_memory_pointer - 1}) ,M({diction.get(temp_name.pop())}) ')
            print(f"+++++++++++++++++++++++++++++++++++++ {p[3]}")

    if (str(type(p[1])) == "<class 'str'>"):
        if len(p) < 3:
            p[0] = p[1]
        else:
            temp_name.append(p[1])
            print(f"append {temp_name}")
            diction_value.update({p[1]: p[3]})
            print(f"diction_value = {diction_value}")

    if len(p) < 3:
        p[0] = p[1]
    elif p[2] == '==':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(get_key_from_value(diction_value, p[1]))}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1



    elif p[2] == '!=':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(get_key_from_value(diction_value, p[1]))}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1


    elif p[2] == '>':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(get_key_from_value(diction_value, p[1]))}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1


    elif p[2] == '<':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:

            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1


    elif p[2] == '>=':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1



    elif p[2] == '<=':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1





    elif p[2] == '*':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1



    elif p[2] == '/':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1



    elif p[2] == '%':
        p[0] = p[1]

        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1




    elif p[2] == '+':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1






    elif p[2] == '-':
        p[0] = p[1]
        if (str(type(p[1])) == "<class 'int'>"):
            output_code.append(
                f'{p[2]}, {p[1]}, {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1
        else:
            output_code.append(
                f'{p[2]}, M({diction.get(p[1])}), {p[3]}, M({temp_memory_pointer})')
            # temp_name.append(f'M({temp_memory_pointer})')
            temp_memory_pointer += 1


    else:
        p[0] = p[1]


def p_primary_expression(p):
    '''primary_expression : INTEGER
                          | FLOAT
                          | CHARACTER
                          | STRING
                          | id_expression
    '''

    if (str(type(p[1])) == "<class 'int'>"):
        number.append(p[1])

    p[0] = p[1]


def p_id_expression(p):
    '''id_expression : IDENTIFIER
             | LPAREN expression RPAREN
    '''

    temp_name.append(p[1])
    print(f"append {temp_name}")

    if len(p) < 3:

        if p[1] in name:
            p[0] = p[1]  # Assign Kardan Value Be Id ke Az Ghabl Mojoode
            u = diction.get(p[1])  # Assign Kardan Address Be Id ke Az Ghabl Mojoode
    else:
        p[0] = p[2]


def p_empty(p):
    'empty :'
    pass


errorcount = 0


def p_error(p):
    global errorcount
    errorcount += 1
    if p:
        col = p.lexpos - code.rfind('\n', 0, p.lexpos) - 1
        print(f"{errorcount}: Syntax error at {p.lineno}:{col} -> ({p.value}) in:")
        print(code_list[p.lineno - 1], end='')
        print(' ' * (col), end='')
        print('^')
    else:  # EOF
        print(f"{errorcount}: Syntax error at EOF")
    print()


y = yacc.yacc()
# for i in range(5):
address = f'D:/Dars/compiler/ali/code{5}.txt'
with open(address) as f:
    code_list = f.readlines()
    code = ''.join(code_list)
print(f'input code #5:')
print(code)
print(f'Parser results for #5:\n')
lineNomber = 0
y.parse(code)

print('Total error count:', errorcount)
print("\n\n")
print(diction)

for count, i in enumerate(output_code):
    print(f'{count}:  {i}')
