from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF2(Node):
    def __init__(self, mnemonic: Mnemonic, op1: int, op2:int=None):
        super().__init__(mnemonic)
        self.op1 = op1
        self.op2 = op2
