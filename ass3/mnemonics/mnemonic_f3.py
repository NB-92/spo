from typing import override

from ass3.code.node import Node
from ass3.code.instruction_f3 import InstructionF3
from ..mnemonics.mnemonic import Mnemonic

# ukazi formata 3 (brez operandov): RSUB
class MnemonicF3(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, parsed_tuple) -> Node:
        label = parsed_tuple[0]
        node = InstructionF3(self, 0)
        if label:
            node.set_label(label)
        return node