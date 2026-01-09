from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f2 import InstructionF2
from mnemonics.mnemonic import Mnemonic

# ukazi formata 2 z enim številskim operandom: SVC
class MnemonicF2n(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, num: int) -> None:
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.num = num

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        operand = operands[0] if operands else None
        return InstructionF2(mnemonic, operand)
