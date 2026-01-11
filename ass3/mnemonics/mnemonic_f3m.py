from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f3 import InstructionF3
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 3 z enim operandom: LDA
class MnemonicF3m(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token
        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        elif len(operands) < 1:
            raise SyntaxError("Missing operand")

        operand: int = operands[0][0]
        node = InstructionF3(self, operand)
        if label:
            node.set_label(label)
        return node