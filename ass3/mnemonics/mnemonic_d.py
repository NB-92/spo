from typing import override

from ass3.code.node import Node
from ass3.code.directive import Directive
from mnemonics.mnemonic import Mnemonic

# Directive without operands
class MnemonicD(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self) -> Node:
        return Directive(self, 0)