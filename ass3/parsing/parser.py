

import ply.yacc

# Lexer.
tokens = (
    'AT',
    'COMMA',
    'HASH',
    'LABEL',
    'REGISTER',
    'MNEMONIC',
    'SYMBOL',
    'NUMBER',
)

t_AT = r'@'
t_COMMA = r','
t_HASH = r'\#'
t_LABEL = r'^[a-z_0-9]+'
t_REGISTER = r'\b[ABFLSTX]\b'
t_MNEMONIC = r'\b[A-Z]+\b'
t_SYMBOL = r'[a-z_0-9]+'

def t_number(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

t_ignore  = ' \t\n'
t_ignore_COMMENT = r'\..*'

def t_error(t):
    print(f'illegal character {t}')
    t.lexer.skip(1)

lexer = ply.lex.lex()

# Parser.
def p_start(p):
    r'''start : LABEL command
            | command'''
    match len(p):
        case 2: p[0] = tuple([None]) + tuple(p[1:])
        case _: p[0] = tuple(p[1:])

def p_command(p):
    r'''command : MNEMONIC
            | MNEMONIC args'''
    p[0] = p[1:]

def p_args(p):
    r'''args : operand
            | operand COMMA operand'''
    match len(p):
        case 2: p[0] = (p[1],)
        case 4: p[0] = (p[1], p[3])

def p_operand(p):
    r'''operand : REGISTER
            | AT address
            | HASH address
            | address'''
    p[0] = p[1:]

def p_address(p):
    r'''address : NUMBER
            | SYMBOL'''
    p[0] = p[1]

def p_error(p):
    if p:
         print('Syntax error at token', p)
         parser.errok()
    else:
         print('Syntax error at EOF')

if __name__ == '__main__':
    import sys
    parser = ply.yacc.yacc()
    for line in sys.stdin:
        print(parser.parse(line))
