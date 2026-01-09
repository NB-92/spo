from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF4(Node):
    def __init__(self, mnemonic: Mnemonic, label: str, comment: str, operand):
        super().__init__(mnemonic)
        self.operand = operand
        self.set_label(label)
        self.set_comment(comment)
