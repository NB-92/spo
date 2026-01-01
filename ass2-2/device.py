
import os

class Device:
    @staticmethod
    def test():
        return True

    def read(self):
        return 0

    def write(self, value):
        pass

# ReadOnly
class InputDevice(Device):
    # used for standard input
    def __init__(self, stream):
        self.stream = stream

    # reads one byte from device
    # returns int
    def read(self):
        val = self.stream.read(1)
        if val:
            return val[0]
        return 0

# WriteOnly
class OutputDevice(Device):
    # used for standard output
    def __init__(self, stream):
        self.stream = stream

    # writes one byte to device
    # receives int
    def write(self, value: int):
        self.stream.write(bytes([value]))
        self.stream.flush()


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