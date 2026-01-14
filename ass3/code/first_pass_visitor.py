from typing import TYPE_CHECKING
from .semantic_error import SemanticError

if TYPE_CHECKING:
    from .directive import Directive
    from .instruction_f1 import InstructionF1
    from .instruction_f2 import InstructionF2
    from .instruction_f3 import InstructionF3
    from .instruction_f4 import InstructionF4
    from .storage import Storage


class FirstPassVisitor:
    def __init__(self, loc_count: int):
        self.location_counter = loc_count
        self.symbol_table = {}
        self.intermediate_table = {}

    def handle_label(self, label):
        if label is not None and label != '':
            if label in self.symbol_table:
                raise ValueError(f"Label '{label}' already in symbol table")
            self.symbol_table[label] = self.location_counter

    def visit_directive(self, node: Directive):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter

        mnemonic = node.get_mnemonic()
        if mnemonic == "ORG":
            self.location_counter = node.operand
        elif mnemonic == "EQU":
            if node.label is None or node.label == '':
                raise SemanticError("EQU directive must have a label")
            self.symbol_table[node.label] = node.operand

    def visit_instruction_f1(self, node: InstructionF1):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter
        self.location_counter += 1  # F1 instruction is 1 byte

    def visit_instruction_f2(self, node: InstructionF2):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter
        self.location_counter += 2  # F1 instruction is 2 byte

    def visit_instruction_f3(self, node: InstructionF3):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter
        self.location_counter += 3  # F1 instruction is 3 byte

    def visit_instruction_f4(self, node: InstructionF4):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter
        self.location_counter += 4  # F4 instruction is 4 byte

    def visit_storage(self, node: Storage):
        self.handle_label(node.label)
        self.intermediate_table[node] = self.location_counter
        if node.mnemonic.name == "BYTE":
            self.location_counter += 1
        elif node.mnemonic.name == "WORD":
            self.location_counter += 3
        elif node.mnemonic.name == "RESB":
            if not isinstance(node.operand, int):
                raise SemanticError("Operand must be an integer")
            self.location_counter += node.operand
        elif node.mnemonic.name == "RESW":
            if not isinstance(node.operand, int):
                raise SemanticError("Operand must be an integer")
            self.location_counter += node.operand * 3
        else:
            raise SemanticError(f"Unknown mnemonic: {node.mnemonic.name}")
