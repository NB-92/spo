from typing import override

from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic


class InstructionF2(Node):
    def __init__(self, mnemonic: Mnemonic, op1, op2=None):
        super().__init__(mnemonic)
        self.op1 = op1
        self.op2 = op2

    def accept(self, visitor):
        visitor.visit_instruction_f2(self)

    @override
    def operand_to_string(self) -> str:
        if self.op2 is not None:
            return f"{self.op1}, {self.op2}"
        else:
            return f"{self.op1}"