from typing import List

import ply.yacc
import ply.lex

from ..code.directive import Directive
from ..code.code import Code
from ..code.node import Node
from ..mnemonics.mnemonic_sn import MnemonicSn
from ..mnemonics.mnemonic_f2rr import MnemonicF2rr
from ..mnemonics.mnemonic_f3 import MnemonicF3
from ..mnemonics.mnemonic_f3m import MnemonicF3m
from ..mnemonics.mnemonic_f4m import MnemonicF4m
from ..mnemonics.mnemonic_sd import MnemonicSd
from ..mnemonics.mnemonic_d import MnemonicD
from ..mnemonics.mnemonic_dn import MnemonicDn
from ..mnemonics.mnemonic_f1 import MnemonicF1
from ..mnemonics.mnemonic_f2n import MnemonicF2n
from ..mnemonics.mnemonic_f2r import MnemonicF2r
from ..mnemonics.mnemonic_f2rn import MnemonicF2rn
from ..mnemonics.mnemonics_table import MnemonicsTable

mnemonics_table = MnemonicsTable()

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
t_MNEMONIC = r'\+?[A-Z]+'
t_SYMBOL = r'[a-z_0-9]+'

def t_NUMBER(t):
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

def parse_text(text):
    parser = ply.yacc.yacc()

    code_list: List[Node] = []
    line_count = 0
    for line in text:
        line_count += 1
        # skip empty lines and comments
        if not line.strip() or line.lstrip().startswith('.'):
            continue

        # and parse all other lines
        line_token = parser.parse(line)
        #print(line_token)

        # get mnemonic, and map it to the correct Mnemonic format
        mnemonic_str = line_token[1][0]
        mnemonic_format = mnemonics_table.get_format(mnemonic_str)
        mnemonic_opcode = mnemonics_table.get_opcode(mnemonic_str)
        #print(mnemonic_str + ": " + mnemonic_format + " " + str(mnemonic_opcode))

        # create the Mnemonic format:
        if mnemonic_str == 'START':
            if len(code_list) > 0:
                raise SyntaxError(f"Error at {line_count}: START must precede all instructions.")

        if mnemonic_format == 'MnemonicD':
            mnemonic = MnemonicD(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicDn':
            mnemonic = MnemonicDn(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF1':
            mnemonic = MnemonicF1(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF2n':
            mnemonic = MnemonicF2n(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF2r':
            mnemonic = MnemonicF2r(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF2rn':
            mnemonic = MnemonicF2rn(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF2rr':
            mnemonic = MnemonicF2rr(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF3':
            mnemonic = MnemonicF3(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF3m':
            mnemonic = MnemonicF3m(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicF4m':
            mnemonic = MnemonicF4m(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicSd':
            mnemonic = MnemonicSd(mnemonic_str, mnemonic_opcode, '', '')
        elif mnemonic_format == 'MnemonicSn':
            mnemonic = MnemonicSn(mnemonic_str, mnemonic_opcode, '', '')
        else:
            raise TypeError(f"Error at {line_count}: Unknown mnemonic format: {mnemonic_format}.")

        # parse line_token and get node and attach node to parsed code
        node = mnemonic.parse(line_token)
        code_list.append(node)

    start_node = code_list[0]
    prog_name = 'null'
    prog_start = 0
    if start_node.mnemonic.name == 'START':
        start_node: Directive
        prog_name = start_node.get_label()
        prog_start = start_node.operand

    code = Code(prog_name, prog_start, code_list)
    return code



if __name__ == '__main__':
    import sys
    parser = ply.yacc.yacc()
    for line in sys.stdin:
        print(parser.parse(line))
