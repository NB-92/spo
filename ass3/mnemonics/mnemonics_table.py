
class MnemonicsTable:
    MNEMONIC_TABLE = {
        # directives
        'NOBASE': ('MnemonicD', -1),
        'LTORG': ('MnemonicD', -1),

        'START': ('MnemonicDn', -1),
        'END': ('MnemonicDn', -1),

        # format 1
        'FIX': ('MnemonicF1', 0xC4),
        'FLOAT': ('MnemonicF1', 0xC0),

        # format 2
        'SVC': ('MnemonicF2n', 0xB0),
        'CLEAR': ('MnemonicF2r', 0xB4),
        'TIXR': ('MnemonicF2r', 0xB8),
        'SHIFTL': ('MnemonicF2rn', 0xA4),
        'SHIFTR': ('MnemonicF2rn', 0xA8),
        'ADDR': ('MnemonicF2rr', 0x90),

        # format 3 / 4
        'ADD': ('MnemonicF3m', 0x18),
        '+ADD': ('MnemonicF4m', 0x18),
        'SUB': ('MnemonicF3m', 0x1C),
        '+SUB': ('MnemonicF4m', 0x1C),
        'MUL': ('MnemonicF3m', 0x20),
        '+MUL': ('MnemonicF4m', 0x20),
        'DIV': ('MnemonicF3m', 0x24),
        '+DIV': ('MnemonicF4m', 0x24),

        'LDA': ('MnemonicF3m', 0x00),
        '+LDA': ('MnemonicF4m', 0x00),
        'STA': ('MnemonicF3m', 0x0C),
        '+STA': ('MnemonicF4m', 0x0C),

        'RSUB': ('MnemonicF3', 0x4C),
        'J': ('MnemonicF3m', 0x3C),

        # storage
        'BYTE': ('MnemonicSd', -2),
        'WORD': ('MnemonicSd', -2),
        'RESB': ('MnemonicSn', -2),
        'RESW': ('MnemonicSn', -2)

    }

    def get_format(self, mnemonic: str) -> str:
        if mnemonic not in self.MNEMONIC_TABLE:
            raise NotImplementedError(f"Unknown mnemonic: {mnemonic}")
        return self.MNEMONIC_TABLE[mnemonic][0]

    def get_opcode(self, mnemonic: str) -> int:
        if mnemonic not in self.MNEMONIC_TABLE:
            raise NotImplementedError(f"Unknown mnemonic: {mnemonic}")
        return self.MNEMONIC_TABLE[mnemonic][1]
