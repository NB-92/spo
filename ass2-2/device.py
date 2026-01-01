
class Device:
    def test(self):
        return True

    def read(self):
        return 0

    def write(self, value):
        pass

# ReadOnly
class InputDevice(Device):
    # used for standard input
    def __int__(self, stream):
        self.stream = stream

    # reads one byte from device
    # returns int
    def read(self):
        val = self.stream.read(1)
        if val:
            return val[0]
        return 0

    # closes stream
    def close(self):
        if self.stream and not self.stream.closed:
            self.stream.close()

# WriteOnly
class OutputDevice(Device):
    # used for standard output
    def __int__(self, stream):
        self.stream = stream

    # writes one byte to device
    # receives int
    def write(self, value: int):
        self.stream.write(bytes([value]))
        self.stream.flush()

    # closes stream
    def close(self):
        if self.stream and not self.stream.closed:
            self.stream.close()

#ReadWrite from file
class FileDevice(Device):
    def __init__(self, num: int):
        # convert int into a 2-digit hexadecimal string (uppercase) XX
        # and create a filename XX.dev
        hex_str = f"{num:02X}"
        filename = f"{hex_str}.dev"

        # checks if ./XX.dev exists and if not, creates an empty file
        if not os.path.exists(filename):
            open(filename, 'wb').close()

        self.stream = open(filename, 'r+b')

    # reads one byte from device
    # returns int
    def read(self):
        val = self.stream.read(1)
        if val:
            return val[0]
        return 0

    # writes one byte to device
    # receives int
    def write(self, value: int):
        self.stream.write(bytes([value]))
        self.stream.flush()

    # closes stream
    def close(self):
        if self.stream and not self.stream.closed:
            self.stream.close()

"""

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
        self.file.flush() """
