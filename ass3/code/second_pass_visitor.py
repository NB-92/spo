from typing import TYPE_CHECKING

from ..mnemonics.mnemonic_f2n import MnemonicF2n
from ..mnemonics.mnemonic_f2r import MnemonicF2r
from ..mnemonics.mnemonic_f2rn import MnemonicF2rn
from .semantic_error import SemanticError
from ..mnemonics.mnemonic_f2rr import MnemonicF2rr

if TYPE_CHECKING:
    from .directive import Directive
    from .instruction_f1 import InstructionF1
    from .instruction_f2 import InstructionF2
    from .instruction_f3 import InstructionF3
    from .instruction_f4 import InstructionF4
    from .storage import Storage


class SecondPassVisitor:
    def __init__(self, symbol_table, intermediate_table):
        self.symbol_table = symbol_table
        self.intermediate_table = intermediate_table
        self.lst_code = [] # for .lst file [(loc, addr, code)]
        self.base_register = None


    @staticmethod
    def is_operand_symbol(operand):
        if isinstance(operand, str):
            return True
        else: return False

    def resolve_operand(self, operand):
        if len(operand) == 1:
            operand = operand[0]
        else:
            operand = operand[1]
        if self.is_operand_symbol(operand):
            if operand in self.symbol_table:
                return self.symbol_table[operand]
            else:
                raise SemanticError(f"Symbol {operand} not found in the symbol table")
        else: return operand

    @staticmethod
    def resolve_register(register):
        match register:
            case 'A': return 0
            case 'X': return 1
            case 'L': return 2
            case 'B': return 3
            case 'S': return 4
            case 'T': return 5
            case 'F': return 6
            case _: raise SemanticError(f"Can't resolve register: {register}")

    # # operandi so oblike ['#', 3] ali ['x'], zato jih je treba pravilno unwrappad
    # def resolve_operand_wrapper(self, operand_wrapped):
    #     if len(operand_wrapped) == 2:
    #         operand = operand_wrapped[1]
    #         operand_wrapped[1] = self.resolve_operand(operand)
    #     else:
    #         operand = operand_wrapped[0]
    #         operand_wrapped[0] = self.resolve_operand(operand)
    #     return operand_wrapped

    # takojšnje #: opcode + 1
    # posredno @: opcode + 2
    # enostavno _: opcode + 3
    @staticmethod
    def resolve_opcode(operand, opcode):
        if len(operand) == 1:
            return opcode + 3
        else:
            sym = operand[0]
            if sym == '#':
                return opcode + 1
            elif sym == '@':
                return opcode + 2
            else:
                raise SemanticError(f"Can't resolve operand: {operand}")

    @staticmethod
    def try_pc_relative(disp):
        if -2048 <= disp <= 2047:
            return True
        else: return False

    def try_base_relative(self, disp):
        if self.base_register is not None:
            if 0 <= disp <= 4095:
                return True
            else: return False
        else: return False

    @staticmethod
    def try_direct(target_addr):
        if 0 <= target_addr <= 4095:
            return True
        else: return False


    # VISIT FUNCTIONS

    def visit_directive(self, node: Directive):
        loc_counter = self.intermediate_table[node]
        mnemonic = node.get_mnemonic()

        if mnemonic == "BASE":
            self.base_register = self.resolve_operand(node.operand)
        elif mnemonic == "NOBASE":
            self.base_register = None


        self.lst_code.append((f"{loc_counter:05X}", None, node))

    def visit_instruction_f1(self, node: InstructionF1):
        loc_counter = self.intermediate_table[node]
        opcode = node.get_opcode()
        self.lst_code.append((f"{loc_counter:05X}", f"{opcode:02X}", node))
        pass

    def visit_instruction_f2(self, node: InstructionF2):
        loc_counter = self.intermediate_table[node]
        opcode = node.get_opcode()  # enostavno naslavljanje
        mnemonic = node.mnemonic

        if isinstance(mnemonic, MnemonicF2rr):
            op1 = self.resolve_register(node.op1)
            op2 = self.resolve_register(node.op2)
        elif isinstance(mnemonic, MnemonicF2n):
            op1 = node.op1
            op2 = node.op2
        elif isinstance(mnemonic, MnemonicF2rn) or isinstance(mnemonic, MnemonicF2r):
            op1 = self.resolve_register(node.op1)
            op2 = node.op2
        else:
            raise SemanticError("Unknown instance of mnemonic")

        combined = (opcode << 8) | ((op1 & 0xF) << 4) | (op2 & 0xF)

        self.lst_code.append((f"{loc_counter:05X}", f"{combined:04X}", node))
        pass

    def visit_instruction_f3(self, node: InstructionF3):
        # če je simbol v simbolni tabeli, operand nadomestimo z naslovom iz simbolne tabele.
        loc_counter = self.intermediate_table[node]
        target_addr = self.resolve_operand(node.operand)
        opcode = self.resolve_opcode(node.operand, node.get_opcode()) if node.operand is not None else node.get_opcode()

        x = 0
        p = 0
        b = 0
        e = 0 # not extended

        if self.try_pc_relative(target_addr - loc_counter - 3):
            p = 1
            disp = target_addr - loc_counter - 3
        elif self.try_base_relative(target_addr - self.base_register):
            b = 1
            disp = target_addr - self.base_register
        elif self.try_direct(target_addr):
            disp = target_addr
        else:
            raise SemanticError(f"Can't reach address: {target_addr}")

        flags = (x << 3) | (b << 2) | (p << 1) | e
        combined = (opcode << 16) | (flags << 12) | (disp & 0xFFF)

        self.lst_code.append((f"{loc_counter:05X}", f"{combined:06X}", node))
        pass

    def visit_instruction_f4(self, node: InstructionF4):
        # če je simbol v simbolni tabeli, operand nadomestimo z naslovom iz simbolne tabele.
        loc_counter = self.intermediate_table[node]
        target_addr = self.resolve_operand(node.operand)
        opcode = self.resolve_opcode(node.operand, node.get_opcode())

        x = 0
        p = 0
        b = 0
        e = 1  # extended

        flags = (x << 3) | (b << 2) | (p << 1) | e
        combined = (opcode << 24) | (flags << 20) | (target_addr & 0xFFFFF)

        self.lst_code.append((f"{loc_counter:05X}", f"{combined:08X}", node))

    def visit_storage(self, node: Storage):
        mnemonic = node.mnemonic.get_name()
        loc_counter = self.intermediate_table[node]

        if mnemonic == "BYTE" or mnemonic == "WORD":
            num = node.operand
        else:
            num = 0
        self.lst_code.append((f"{loc_counter:05X}", f"{num:06X}", node))
        pass