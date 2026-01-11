
from ass3.code.node import Node

class Code:
    def __init__(self, prog_name: str, prog_start: int, code: list[Node]):
        self.prog_name = prog_name
        self.prog_start = prog_start

        self.loc = prog_start
        self.next_loc = prog_start
        self.regB = -1

        self.program = code

    def to_string(self):
        return "\n".join(node.to_string() for node in self.program)


    def begin(self):
        self.loc = self.prog_start
        self.next_loc = self.prog_start
        self.regB = -1

    def end(self):
        pass

    # resolving symbols
    def resolve(self):
        self.begin()
        for node in self.program:
            node.enter(self)
            node.resolve(self)
            node.leave(self)
        length = self.next_loc - self.prog_start
        self.end()

    # generating object file
    def dump_text(self):
        pass

    # generating raw code
    def dump_code(self):
        pass
