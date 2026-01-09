from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f2 import InstructionF2
from mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z dvema registerskima operandoma: ADDR
class MnemonicF2rr(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, reg1: int, reg2: int):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.reg1 = reg1
        self.reg2 = reg2

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        operand_1 = operands[0] if operands else None
        operand_2 = operands[1] if operands else None
        return InstructionF2(mnemonic, operand_1, operand_2)