from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f2 import InstructionF2
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z enim številskim operandom: SVC
class MnemonicF2n(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str) -> None:
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token
        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        elif len(operands) < 1:
            raise SyntaxError("Missing operand")

        operand = operands[0][0]
        node = InstructionF2(self, operand, 0)
        if label:
            node.set_label(label)
        return node
