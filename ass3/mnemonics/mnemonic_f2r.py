from typing import override

from ass3.code.node import Node

from ass3.code.instruction_f2 import InstructionF2
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z enim registerskim operandom: CLEAR, TIXR
class MnemonicF2r(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token

        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        elif len(operands) < 1:
            raise SyntaxError("Missing operand")

        operand: str = operands[0][0]
        if not isinstance(operand, str):
            raise SyntaxError("Invalid operand")
        node = InstructionF2(self, operand, 0)
        if label:
            node.set_label(label)
        return node