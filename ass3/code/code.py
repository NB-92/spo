
from ass3.code.node import Node
from .first_pass_visitor import FirstPassVisitor
from .second_pass_visitor import SecondPassVisitor


class Code:
    def __init__(self, prog_name: str, prog_start: int, code: list[Node]):
        self.prog_name = prog_name
        self.prog_start = prog_start
        self.prog_len = 0

        self.program = code

        self.symbol_table = {}
        self.intermediate_table = {} # Node: prog_location

        self.lst_code = []
        self.object_program = ""

    def first_pass(self):
        visitor = FirstPassVisitor(self.prog_start)

        for node in self.program:
            node.accept(visitor)

        self.prog_len = visitor.location_counter - self.prog_start
        self.symbol_table = visitor.symbol_table
        self.intermediate_table = visitor.intermediate_table
        return self.symbol_table

    def second_pass(self):
        visitor = SecondPassVisitor(self.symbol_table, self.intermediate_table)

        text_record:str
        for node in self.program:
            node.accept(visitor)

        self.lst_code = visitor.lst_code
        self.object_program = self.get_obj_code()

    def lst_to_string(self):
        lines = []
        for lst_tuple in self.lst_code:
            addr: str = lst_tuple[1] if lst_tuple[1] is not None else "      "
            line: str = lst_tuple[0] + " " + addr + " " + lst_tuple[2].to_string()
            lines.append(line)
        return "\n".join(lines)

    def get_obj_code(self):
        """Generates the full object program string (Header, Text, End records)."""
        object_program = self.get_header()

        text_records = []
        current_text = ""
        current_start_addr = None
        current_length = 0

        for loc_str, code_str, node in self.lst_code:
            if code_str is None or code_str == "" or node.get_mnemonic() == "RESW" or node.get_mnemonic() == "RESB":  # skip directives like BASE, NOBASE as well as RESW and RESB
                continue

            if current_start_addr is None:
                current_start_addr = int(loc_str, 16)

            # Check if adding this code exceeds 30 bytes
            if current_length + len(code_str)//2 > 30:
                # Finish current text record
                text_records.append(self.make_text_record(current_start_addr, current_text))
                # Start new record
                current_start_addr = int(loc_str, 16)
                current_text = code_str
                current_length = len(code_str)//2
            else:
                current_text += code_str
                current_length += len(code_str)//2

        # Add the last text record
        if current_text:
            text_records.append(self.make_text_record(current_start_addr, current_text))

        # Append text records
        object_program += "".join(text_records)

        # End record
        object_program += self.get_end_record()

        return object_program

    @staticmethod
    def make_text_record(start_addr, object_codes):
        length = len(object_codes) // 2
        return f"T{start_addr:06X}{length:02X}{object_codes}\n"

    def get_end_record(self):
        return f"E{self.prog_start:06X}\n"


    def get_header(self):
        return f"H{self.prog_name.ljust(6, " ")}{self.prog_start:06X}{self.prog_len:06X}\n"


    def to_string(self):
        return "\n".join(node.to_string() for node in self.program)
