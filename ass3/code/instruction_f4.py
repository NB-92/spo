from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF4(Node):
    def __init__(self, mnemonic: Mnemonic, operand):
        super().__init__(mnemonic)
        self.operand = operand
