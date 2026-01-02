
class Utils:

    @staticmethod
    def read_string(reader, length: int) -> str:
        string = reader.read(length)
        if len(string) != length:
            raise EOFError("Unexpected EOF")
        return string

    @staticmethod
    def read_byte(reader) -> int:
        # reads two hex symbols and returns a byte
        string = Utils.read_string(reader, 2)
        return int(string, 16)

    @staticmethod
    def read_word(reader) -> int:
        # reads 6 hex symbols and returns a 24-bit word
        string = Utils.read_string(reader, 6)
        return int(string, 16)

