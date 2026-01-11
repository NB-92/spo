from typing import override

from ..code.node import Node
from ..code.directive import Directive
from ..mnemonics.mnemonic import Mnemonic

# Directive without operands: NOBASE, LTORG
class MnemonicD(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)

    @override
    def parse(self, parsed_tuple) -> Node:
        label = parsed_tuple[0]
        node = Directive(self)
        if label:
            node.set_label(label)
        return node