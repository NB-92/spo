from typing import override, TYPE_CHECKING

from ass3.code.node import Node
from .semantic_error import SemanticError

if TYPE_CHECKING:
    from ass3.mnemonics.mnemonic import Mnemonic
    from ..mnemonics.mnemonic_sd import MnemonicSd


# Storage directives: BYTE, WORD, RESB, RESW
class Storage(Node):
    def __init__(self, mnemonic: Mnemonic, operand):
        super().__init__(mnemonic)
        self.operand = operand

    def accept(self, visitor):
        visitor.visit_storage(self)


    @override
    def operand_to_string(self) -> str:
        if self.operand is not None:
            return f"{self.operand}"
        return ""