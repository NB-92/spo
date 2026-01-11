
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
        return self.label + " " + self.mnemonic.to_string() + " " + self.operand_to_string() + " " + self.comment

    def operand_to_string(self):
        return ""

    # poklicemo vsakic, ko med obhodom zacnemo in koncamo z obdelavo
    # posamicnega vozlisca (Node)
    def enter(self):
        # code.loc = code.next_loc
        # if self.length() < 0:
        #     raise ValueError("Length of code must be >= 0")
        # code.next_loc = code.next_loc + self.length()
        pass

    def leave(self):
        # directive ORG
        pass

    # vrne dolzino v bajtih
    def length(self) -> int:
        return -1