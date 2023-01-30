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

# type name = val
names = {}
types = {}
addrs = {}
ids = []

tmp_addr = None
ss = []
output_code = []
DM_ptr = 100  # keep pointer of Data Memory address
TD_ptr = 500  # keep pointer of Temporary Data memory address

### STATEMENTS ###

start = 'statement_list'


def p_statement(p):
    '''statement : compound_statement
                 | declaration_statement
                 | selection_statement
                 | iteration_statement
                 | expression_statement
                 | print_statement
                 | SEMICOLON'''
    p[0] = p[1]


def p_compound_statement(p):  ##
    'compound_statement : LBRACE statement_list RBRACE'
    p[0] = p[2]


def p_statement_list(p):  ##
    '''statement_list : statement_list statement 
                      | empty'''


##############
def p_declaration_statement(p):
    'declaration_statement : type_specifier declaration_list SEMICOLON'

    global DM_ptr, tmp_addr
    lineno = p.slice[3].lineno
    for i in ids:
        if i in names:

            type2 = str(type(names[i])).split("'")[1]
            type1 = {'int': 'int', 'float': 'float', 'char': 'str', 'string': 'str'}
            if type1[p[1]] == type2:
                if p[1] == 'char' and len(names[i]) > 1:
                    print(
                        f"'char' variable can't be initialize with 'string' value at line {lineno}. {i}")
                    names.pop(i, None)
                    continue

                types[i] = p[1]
                addrs[i] = DM_ptr
                DM_ptr += 1

                # mem(x) -> value in x posision of memory
                # x -> value x itself
                if tmp_addr:
                    output_code.append(f':=, M({ss.pop()}), M({addrs[i]}), ')
                else:
                    output_code.append(f':=, {ss.pop()}, M({addrs[i]}), ')
            else:
                if type2 == 'str':
                    type2 = 'char'
                    if len(names[i]) > 1:
                        type2 = 'string'

                print(f"'{p[1]}' variable can't be initialize with '{type2}' value at line {lineno}. {i}")
                names.pop(i, None)

        else:
            names[i] = None
            types[i] = p[1]
            addrs[i] = DM_ptr
            DM_ptr += 1
    ids.clear()
    tmp_addr = None


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
                            | IDENTIFIER OP_assign equality_expression
    '''
    if len(p) > 2:
        lineno = p.slice[2].lineno
    if not (p[1] in names or p[1] in ids):
        ids.append(p[1])
        if len(p) > 2:
            names[p[1]] = p[3]
    else:
        print(f"Redefinition of '{p[1]}' at line {lineno}.")


##############

def p_print_statement(p):
    'print_statement : KEY_print LPAREN expression RPAREN SEMICOLON'
    output_code.append(f'PRT, {ss.pop()}, , ')
    print('>', p[3])


def p_selection_statement(p):
    '''selection_statement : KEY_if LPAREN expression save RPAREN statement
                           | KEY_if LPAREN expression save RPAREN statement KEY_else save statement'''
    if len(p) < 8:  # IF
        index = ss.pop()
        output_code[index] = f'JPF, {ss.pop()}, M({len(output_code)}), '

    else:  # IF ELSE
        index = ss.pop()
        output_code[index] = f'JP, {1}, M({len(output_code)}), '
        index2 = ss.pop()
        output_code[index2] = f'JPF, {ss.pop()}, M({index + 1}), '


def p_iteration_statement(p):
    '''iteration_statement : KEY_while label LPAREN expression save RPAREN statement
                           | KEY_do label statement KEY_while LPAREN expression RPAREN SEMICOLON
                           | KEY_for LPAREN optexpr label SEMICOLON optexpr save SEMICOLON optexpr RPAREN statement'''

    if p[1] == 'while':
        index = ss.pop()
        output_code[index] = f'JPF, {ss.pop()}, M({len(output_code) + 1}), '
        output_code.append(f'JP, {ss.pop()}, , ')

    if p[1] == 'do':
        output_code.append(f'JPF, {ss.pop()}, M({ss.pop()}), ')
        ss.pop()

    if p[1] == 'for':
        index = ss.pop()
        output_code[index] = f'JPF, {ss.pop()}, M({len(output_code) + 1}), '
        output_code.append(f'JP, {ss.pop()}, , ')


def p_label(p):
    'label : empty'
    ss.append(len(output_code))


def p_save(p):
    'save : empty'
    ss.append(len(output_code))
    output_code.append(f'save')


def p_optexpr(p):
    '''optexpr : assignment_expression
               | empty
    '''


def p_expression_statement(p):
    'expression_statement : expression SEMICOLON'


### EXPRESSIONS ###

def p_expression(p):
    '''expression : assignment_expression
                  | expression COMMA assignment_expression
    '''
    if len(p) < 3:
        p[0] = p[1]


def p_assignment_expression(p):
    '''assignment_expression : equality_expression
                             | IDENTIFIER OP_assign equality_expression
    '''
    global tmp_addr
    if len(p) < 3:
        p[0] = p[1]
    else:
        lineno = p.slice[1].lineno
        type1 = str(type(p[3])).split("'")[1]
        type2 = str(type(names[p[1]])).split("'")[1]
        if type(names[p[1]]) == type(None):
            type2 = type1
        if not p[1] in names:  # not exist
            print(f'The variable <{p[1]}> is not defined at line {lineno}.')

        elif type1 != type2:  # wrong type            
            print(f"'{type1}' value can't be assign to <{p[1]}> with type of '{type2}' at line {lineno}.")

        else:
            names[p[1]] = p[3]
            if tmp_addr:
                output_code.append(f':=, M({ss.pop()}), M({addrs[p[1]]}), ')
            else:
                output_code.append(f':=, {ss.pop()}, M({addrs[p[1]]}), ')

    tmp_addr = None


def p_equality_expression(p):
    '''equality_expression : relational_expression
                           | equality_expression OP_equal relational_expression
                           | equality_expression OP_notequal relational_expression
    '''
    if len(p) < 3:
        p[0] = p[1]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
        generate('==')
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
        generate('!=')


def p_relational_expression(p):
    '''relational_expression : additive_expression
                             | relational_expression OP_greater additive_expression 
                             | relational_expression OP_less additive_expression
                             | relational_expression OP_greaterequal additive_expression
                             | relational_expression OP_lessequal additive_expression
    '''
    if len(p) < 3:
        p[0] = p[1]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
        generate('>')
    elif p[2] == '<':
        p[0] = p[1] < p[3]
        generate('<')
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
        generate('>=')
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
        generate('<=')


def p_additive_expression(p):
    '''additive_expression : multiplicative_expression 
                           | additive_expression OP_add multiplicative_expression
                           | additive_expression OP_subtract multiplicative_expression
    '''
    global TD_ptr
    if len(p) < 3:
        p[0] = p[1]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
        generate('+')
    elif p[2] == '-':
        p[0] = p[1] - p[3]
        generate('-')


def p_multiplicative_expression(p):
    '''multiplicative_expression : unary_expression
                                 | multiplicative_expression OP_multiply unary_expression
                                 | multiplicative_expression OP_divide unary_expression
                                 | multiplicative_expression OP_mod unary_expression
    '''
    global tmp_addr, TD_ptr
    if len(p) < 3:
        p[0] = p[1]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
        generate('*')
    elif p[2] == '/':
        p[0] = p[1] / p[3]
        generate('/')
    elif p[2] == '%':
        p[0] = p[1] % p[3]
        generate('%')

    tmp_addr = None


def p_unary_expression(p):
    '''unary_expression : primary_expression
                        | OP_subtract primary_expression %prec OP_negate'''
    if len(p) > 2:
        p[0] = -p[2]
    else:
        p[0] = p[1]


def p_primary_expression(p):
    '''primary_expression : INTEGER
                          | FLOAT
                          | CHARACTER
                          | STRING
                          | id_expression
    '''
    if tmp_addr:
        ss.append(f'M({tmp_addr})')
    else:
        ss.append(p[1])
    p[0] = p[1]


def p_id_expression(p):
    '''id_expression : IDENTIFIER
             | LPAREN expression RPAREN
    '''
    global tmp_addr
    if len(p) < 3:
        if p[1] in names:
            p[0] = names[p[1]]
            tmp_addr = addrs[p[1]]
    else:
        p[0] = p[2]


def p_empty(p):
    'empty :'
    pass


def generate(op):
    global TD_ptr
    output_code.append(f'{op}, {ss.pop(-2)}, {ss.pop()}, M({TD_ptr})')
    ss.append(f'M({TD_ptr})')
    TD_ptr += 1


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
for i in range(5):
    address = f'D:/Dars/compiler/ali/New folder/code3.txt'
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
print(names)
print(types)
print(addrs)
for count, i in enumerate(output_code):
    print(f'{count}:  {i}')
