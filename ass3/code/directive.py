from typing import override

from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic

# Directives: START, END, ...
class Directive(Node):
    def __init__(self, mnemonic: Mnemonic, operand=None):
        Node.__init__(self, mnemonic)
        self.operand = operand

    def accept(self, visitor):
        visitor.visit_directive(self)

    @override
    def operand_to_string(self) -> str:
        if self.operand is not None:
            return f"{self.operand}"
        return ""