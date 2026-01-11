from typing import override

from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic


class InstructionF1(Node):
    def __init__(self, mnemonic: Mnemonic):
        super().__init__(mnemonic)

    # vrne dolzino v bajtih
    def length(self) -> int:
        return 1
