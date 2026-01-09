from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF2(Node):
    def __init__(self, mnemonic: Mnemonic, label: str, comment: str, reg1: int, reg2: int):
        super().__init__(mnemonic)
        self.reg1 = reg1
        self.reg2 = reg2
        self.set_label(label)
        self.set_comment(comment)
