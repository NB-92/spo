from typing import override

from ass3.code.node import Node
from ass3.code.directive import Directive
from ..mnemonics.mnemonic import Mnemonic


# Directive with one numeric operand: START, END
class MnemonicDn(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token
        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        elif len(operands) < 1:
            raise SyntaxError("Missing operand")

        operand:str = operands[0][0]
        if not isinstance(operand, int):
            raise SyntaxError("Invalid operand")
        node = Directive(self, operand)
        if label:
            node.set_label(label)
        return node

    def operand_to_string(self, instruction: Node):
        pass