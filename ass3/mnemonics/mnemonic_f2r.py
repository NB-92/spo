from typing import override

from ass3.code.node import Node

from ass3.code.instruction_f2 import InstructionF2
from mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z enim registerskim operandom: CLEAR, TIXR
class MnemonicF2r(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, reg:int):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.reg = reg

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        operand = operands[0] if operands else None
        return InstructionF2(mnemonic, operand)