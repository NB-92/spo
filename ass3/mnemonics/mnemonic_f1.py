from typing import override

from ass3.code.instruction_f1 import InstructionF1
from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 1 (brez operandov): FIX, FLOAT
class MnemonicF1(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, parsed_tuple) -> Node:
        label = parsed_tuple[0]
        node = InstructionF1(self)
        if label:
            node.set_label(label)
        return node