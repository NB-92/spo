from typing import override

from ..code.node import Node
from ..code.storage import Storage
from ..mnemonics.mnemonic import Mnemonic

# pomnilniŠka direktvia za rezervacijo: RESB, RESW
class MnemonicSn(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, line_token) -> Node:
        label, [_, operands] = line_token
        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        elif len(operands) < 1:
            raise SyntaxError("Missing operand")

        operand = operands[0][0]
        node = Storage(self, operand)
        if label:
            node.set_label(label)
        return node