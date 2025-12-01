
class Device:

    def test(self) -> bool:
        return True

    def read(self) -> int:
        return 0

    def write(self, value):
        pass

class InputDevice(Device):
    def __init__(self, stream):
        self.reader = stream

    def read(self) -> int:
        data = self.reader.read(1)
        if data:
            return data[0]
        return 0

class OutputDevice(Device):
    def __init__(self, stream):
        self.writer = stream

    def write(self, value: int):
        self.writer.write(bytes([value]))
        self.writer.flush()

class FileDevice(Device):
    def __init__(self, filename, mode='r+b'):
        self.file = open(filename, mode)

    def read(self) -> int:
        data = self.file.read(1)
        if data:
            return data[0]
        return 0

    def write(self, value: int):
        self.file.write(bytes([value]))
        self.file.flush()