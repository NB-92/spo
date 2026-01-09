
"""
    Abstract class Node.
    Includes label, mnemonic and comment
"""
from ass3.mnemonics.mnemonic import Mnemonic


class Node:
    def __init__(self, mnemonic: Mnemonic):
        self.label: str = ""
        self.mnemonic = mnemonic
        self.comment: str = ""

    def get_label(self):
        return self.label

    def set_label(self, label: str):
        self.label = label

    def get_comment(self):
        return self.comment

    def set_comment(self, comment: str):
        self.comment = comment

    def to_string(self):
        return self.mnemonic.to_string(self.mnemonic) + " " + self.operand_to_string()

    def operand_to_string(self):
        return self.mnemonic.operand_to_string(self)