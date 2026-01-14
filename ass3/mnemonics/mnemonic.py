
class Mnemonic:
    def __init__(self, name: str, opcode: int, hint: str, desc: str):
        self.name = name
        self.opcode = opcode
        self.hint = hint
        self.desc = desc

    def get_name(self):
        return self.name

    # prebere operande iz parserja
    # vrne ukazni razred node ustreznega razreda
    def parse(self, parsed_tuple) -> Node:
        from ..code.node import Node
        return None

    def to_string(self):
        return f"  {self.name}"


