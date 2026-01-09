from ass3.code.node import Node


class Mnemonic:
    def __init__(self, name: str, opcode: int, hint: str, desc: str):
        self.name = name
        self.opcode = opcode
        self.hint = hint
        self.desc = desc

    # prebere operande iz parserja
    # vrne ukazni razred node ustreznega razreda
    def parse(self, parsed_tuple) -> Node:
        return None

    def to_string(self):
        return f"name:<6"

    def operand_to_string(self, instruction: Node):
        return ""