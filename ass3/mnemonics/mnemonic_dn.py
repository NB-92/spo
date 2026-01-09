from typing import override

import parsing.parser as parser
from ass3.code.node import Node
from ass3.code.directive import Directive
from mnemonics.mnemonic import Mnemonic


# Directive with one numeric operand: START, END
class MnemonicDn(Mnemonic):
    def __init__(self, mnemonic: str, opcode: int, hint: str, desc: str, num: int):
        Mnemonic.__init__(self, mnemonic, opcode, hint, desc)
        self.num_operand = num

    @override
    def parse(self, parsed_tuple) -> Node:
        mnemonic, operands = parsed_tuple
        if len(operands) > 1:
            raise SyntaxError("Too many operands")
        operand = operands[0] if operands else None
        return Directive(mnemonic, operand)

    @override
    def operand_to_string(self, instruction: Node):
        i: Directive = instruction
        return i.symbol if i.symbol is not None else str(i.value)