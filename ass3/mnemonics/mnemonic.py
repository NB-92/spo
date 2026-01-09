from ass3.code.node import Node


class Mnemonic:
    def __init__(self, name: str, opcode: int, hint: str, desc: str):
        self.name = name
        self.opcode = opcode
        self.hint = hint
        self.desc = desc

    def parse(self) -> Node:
        return Node(None)

    def to_string(self):
        return f"name:<6"

    def operand_to_string(self, instruction: Node):
        return ""