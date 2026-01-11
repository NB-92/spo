from typing import override

from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic


class InstructionF3(Node):
    def __init__(self, mnemonic: Mnemonic, operand=None):
        super().__init__(mnemonic)
        self.operand = operand

    # vrne dolzino v bajtih
    def length(self) -> int:
        return 3

    @override
    def operand_to_string(self) -> str:
        if self.operand is not None:
            return f"{self.operand}"
        return ""
