from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF3(Node):
    def __init__(self, mnemonic: Mnemonic, operand=None):
        super().__init__(mnemonic)
        self.operand = operand

