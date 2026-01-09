from ass3.code.node import Node
from mnemonics.mnemonic import Mnemonic


class InstructionF1(Node):
    def __init__(self, mnemonic: Mnemonic, label: str, comment: str):
        super().__init__(mnemonic)
        self.set_label(label)
        self.set_comment(comment)
