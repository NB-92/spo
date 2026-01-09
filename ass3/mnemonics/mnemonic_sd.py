
from typing import override

from ass3.code.node import Node
from ass3.code.storage import Storage
from mnemonics.mnemonic import Mnemonic

# pomnilniŠka direktvia s podatki: BYTE; WORD
class MnemonicSd(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, operand: int):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.operand = operand

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        operand = operands[0] if operands else None
        return Storage(mnemonic, operand)