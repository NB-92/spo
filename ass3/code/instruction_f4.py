from typing import override

from ass3.code.node import Node
from ..mnemonics.mnemonic import Mnemonic


class InstructionF4(Node):
    def __init__(self, mnemonic: Mnemonic, operand=None):
        super().__init__(mnemonic)
        self.operand = operand

    def accept(self, visitor):
        visitor.visit_instruction_f4(self)

    @override
    def operand_to_string(self) -> str:
        if self.operand is not None:
            if len(self.operand) > 1:
                return f"{self.operand[0]}{str(self.operand[1])}"
            else:
                return f"{self.operand[0]}"
        return ""
