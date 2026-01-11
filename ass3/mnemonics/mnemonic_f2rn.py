from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f2 import InstructionF2
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z enim registerskim in enim stevilskim operandom: SHIFTL, SHIFTR
class MnemonicF2rn(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token
        if len(operands) > 2:
            raise SyntaxError("Too many operands")
        elif len(operands) < 2:
            raise SyntaxError("Missing operand")

        reg1: str = operands[0][0]
        n: int = operands[0][1]
        node = InstructionF2(self, reg1, n)
        if label:
            node.set_label(label)
        return node