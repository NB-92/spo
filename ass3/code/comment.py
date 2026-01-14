from typing import override
from node import Node

class Comment(Node):
    def __init__(self, comment: str):
        Node.__init__(self, None)
        self.set_comment(comment)

    @override
    def to_string(self):
        return self.comment
