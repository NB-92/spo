from typing import override

import parsing.parser as parser
from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


# Directive with one numeric operand
class MnemonicDn(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self) -> Node:
        # number
        tok = parser.lexer.token()
        if tok.type == 'NUMBER':
            return Directive(self, tok.value)
        # symbol
        elif tok.type == 'SYMBOL':
            return Directive(self, tok.value)
        # otherwise: error
        else:
            char = parser.lexer.peek()
            raise SyntaxError(
                f"Invalid character '{tok.value}'",
                ("<string>", parser.lexer.lineno, parser.lexer.lexpos, "")
            )

    @override
    def operand_to_string(self, instruction: Node):
        i: Directive = instruction
        return i.symbol if i.symbol != None else str(i.value)