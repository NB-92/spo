
"""
    Abstract class Node.
    Includes label, mnemonic and comment
"""
from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ass3.mnemonics.mnemonic import Mnemonic


class Node(ABC):
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

    def get_mnemonic(self):
        return self.mnemonic.get_name()

    @abstractmethod
    def accept(self, visitor):
        pass

    def to_string(self):
        return self.label + " " + self.mnemonic.to_string() + " " + self.operand_to_string() + " " + self.comment

    def operand_to_string(self):
        return ""

    def get_opcode(self):
        return self.mnemonic.opcode

    # # poklicemo , ko med obhodom zacnemo z obdelavo posamicnega ukaza (Node)
    # def enter(self, code: Code):
    #     pass
    #
    # # poklicemo , ko med obhodom končamo z obdelavo posamicnega ukaza (Node)
    # def leave(self, code: Code):
    #     pass
    #
    # # vrne dolzino v bajtih
    # def length(self) -> int:
    #     return -1