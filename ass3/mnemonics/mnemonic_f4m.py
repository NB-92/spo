from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f4 import InstructionF4
from mnemonics.mnemonic import Mnemonic

# ukazi formata 4 z enim operandom: +LDA
class MnemonicF4m(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, operand: int):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.operand = operand

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        operand = operands[0] if operands else None
        return InstructionF4(mnemonic, operand)