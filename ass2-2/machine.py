
import sys
from typing import List, Optional, Union
from device import Device, InputDevice, OutputDevice, FileDevice
from sic_opcode import Opcode
from utils import Utils

MAX_ADDRESS = 2 ** 20  # naslovni prostor (20-bitov)

class Machine:

    def __init__(self):
        self.running = False

        # POMNILNIK
        self.memory = bytearray(MAX_ADDRESS)

        # REGISTRI
        self.regs: List[Union[int, float]] = [0] * 10  # [A, X, L, B, S, T, F, -, PC, SW]
        # Za register SW nas zanimata le bita CC:
        # 0x00 - manjse
        # 0x40 - enako
        # 0x80 - vecje
        self.regs[6] = 0.0  # register F bo float
        self.reset()

        # NAPRAVE
        # SIC/XE podpira 256 naprav
        self.devices: List[Optional[Device]] = [None] * 256

        # Standardni vhod, izhod in izhod za napake
        self.devices[0] = InputDevice(sys.stdin.buffer)
        self.devices[1] = OutputDevice(sys.stdout.buffer)
        self.devices[2] = OutputDevice(sys.stderr.buffer)


    def reset(self):
        self.regs = [0] * 10 # [A, X, L, B, S, T, F, -, PC, SW]
        self.regs[6] = 0.0 # register F bo float

    # DOSTOP DO REGISTROV
    def get_a(self) -> int: return self.regs[0]
    def set_a(self, val): self.regs[0] = val

    def get_x(self) -> int: return self.regs[1]
    def set_x(self, val): self.regs[1] = val

    def get_l(self) -> int: return self.regs[2]
    def set_l(self, val): self.regs[2] = val

    def get_b(self) -> int: return self.regs[3]
    def set_b(self, val): self.regs[3] = val

    def get_s(self) -> int: return self.regs[4]
    def set_s(self, val): self.regs[4] = val

    def get_t(self) -> int: return self.regs[5]
    def set_t(self, val): self.regs[5] = val

    def get_f(self) -> int: return self.regs[6]
    def set_f(self, val): self.regs[6] = val

    def get_pc(self) -> int: return self.regs[8]
    def set_pc(self, val): self.regs[8] = val

    def get_sw(self) -> int: return self.regs[9]
    def set_sw(self, val): self.regs[9] = val

    # dostop do vrednosti po indeksu
    def get_reg(self, index) -> int: return self.regs[index]
    def set_reg(self, index, val):
        if index == 6:
            self.regs[6] = float(val)
        else: self.regs[index] = val

    # DOSTOP DO POMNILNIKA
    def get_byte(self, addr):
        if 0 <= addr < MAX_ADDRESS:
            return self.memory[addr]
        else:
            self.invalid_addressing()
            raise ValueError("Naslov izven meja.")

    def set_byte(self, addr, val):
        if 0 <= addr < MAX_ADDRESS:
            self.memory[addr] = val
        else:
            self.invalid_addressing()
            raise ValueError("Naslov izven meja.")

    def get_word(self, addr):
        if 0 <= addr <= MAX_ADDRESS - 3:
            return (self.memory[addr] << 16) | (self.memory[addr + 1] << 8) | (self.memory[addr + 2])
        else:
            self.invalid_addressing()
            raise ValueError("Naslov izven meja.")

    def set_word(self, addr, val):
        if 0 <= addr < MAX_ADDRESS - 3:
            self.memory[addr] = (val >> 16) & 0xFF # ohrani samo spodnji Byte
            self.memory[addr + 1] = (val >> 8) & 0xFF
            self.memory[addr + 2] = val & 0xFF
            return (self.memory[addr] << 16) | (self.memory[addr+1] << 8) | (self.memory[addr+2])
        else:
            self.invalid_addressing()
            raise ValueError(f"Naslov {addr} izven meja.")

    # SAMODEJNO IZVAJANJE
    def start(self):
        self.running = True
        try:
            while self.running:
                if not self.execute():
                    self.stop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False

    def step(self):
        return self.execute()

    # IZVAJALNIK
    # naloži in vrne en bajt iz naslova PC in poveča PC za 1
    def fetch(self) -> int:
        pc = self.get_pc()
        self.set_pc(pc + 1)
        return self.get_byte(pc)

    #dekodira ukaz in morebitne operande z naslova PC ter ga izvede
    def execute(self):
        op = Opcode()

        opcode_byte = self.fetch()
        ni_bits = opcode_byte & 0x03 # n = bit1, i = bit0
        opcode = opcode_byte & 0xFC # zgornjih 6 bitov

        sic_format = op.get_format(opcode)
        if sic_format == -1:
            self.invalid_opcode(opcode)
            return False
        elif sic_format == 1:
            self.execute_f1(opcode)
        elif sic_format == 2:
            operand = self.fetch()
            self.execute_f2(opcode, operand)
        elif sic_format == 3:
            byte2 = self.fetch()
            byte3 = self.fetch()
            operand = (byte2 << 8) | byte3
            self.execute_f3f4(opcode, ni_bits, operand)
        return True

    def execute_f1(self, opcode: int) -> bool:
        op = Opcode()
        mnemonic = op.get_mnemonic(opcode)

        if mnemonic == "":
            self.invalid_opcode(opcode)
            return False

        if mnemonic == "FIX": self.fix()
        elif mnemonic == "FLOAT": self.float()
        else:
            self.not_implemented(mnemonic)
            return False
        return True

    def execute_f2(self, opcode: int, operand: int) -> bool:
        r2 = operand & 0x0F # spodnji 4 biti
        r1 = (operand >> 4) & 0xF # zgornji 4 biti

        op = Opcode()
        mnemonic = op.get_mnemonic(opcode)

        if mnemonic == "":
            self.invalid_opcode(opcode)
            return False

        if mnemonic == "ADDR": self.add_r(r1, r2)
        elif mnemonic == "SUBR": self.sub_r(r1, r2)
        elif mnemonic == "MULR": self.mul_r(r1, r2)
        elif mnemonic == "RMO": self.rmo(r1, r2)
        elif mnemonic == "DIVR": self.div_r(r1, r2)
        elif mnemonic == "COMPR": self.comp_r(r1, r2)
        else:
            self.not_implemented(mnemonic)
            return False
        return True

    def execute_f3f4(self, opcode: int, ni: int, operand: int) -> bool:
        op = Opcode()
        mnemonic = op.get_mnemonic(opcode)

        if mnemonic == "":
            self.invalid_opcode(opcode)
            return False

        x_bit = (operand & 15) & 1
        b_bit = (operand >> 14) & 1
        p_bit = (operand >> 13) & 1
        e_bit = (operand & 12) & 1
        disp = operand & 0x0FFF

        # FORMAT 4 (extended)
        if e_bit == 1:
            byte4 = self.fetch()
            addr = (disp << 8) | byte4

        # FORMAT 3
        else:
            if p_bit == 1:
                # PC-relative
                if disp & 0x800:
                    disp -= 0x1000
                addr = self.get_pc() + disp
            elif b_bit == 1:
                # base-relative
                addr = self.get_b() + disp
            else:
                # Direct
                addr = disp

        if ni == 0x00:
            # SIC compatibility (simple)
            val = self.get_word(addr)
        elif ni == 0x03:
            # Simple addressing
            if x_bit == 1:
                addr += self.get_x()
            val = self.get_word(addr)
        elif ni == 0x02:
            # Indirect
            if x_bit == 1:
                self.invalid_addressing()
                return False
            ptr = self.get_word(addr)
            val = self.get_word(ptr)
        elif ni == 0x01:
            # Immediate
            if x_bit == 1:
                self.invalid_addressing()
                return False
            val = addr
        else:
            self.invalid_addressing()
            return False

        if mnemonic == "ADD":
            self.add(val)
        elif mnemonic == "AND":
            self.sic_and(val)
        elif mnemonic == "OR":
            self.sic_or(val)
        elif mnemonic == "COMP":
            self.comp(val)
        elif mnemonic == "DIV":
            self.div(val)
        elif mnemonic == "J":
            self.jump(addr)
        elif mnemonic == "JEQ":
            self.jeq(addr)
        elif mnemonic == "JGT":
            self.jgt(addr)
        elif mnemonic == "JLT":
            self.jlt(addr)
        elif mnemonic == "JSUB":
            self.jsub(addr)
        elif mnemonic == "LDA":
            self.lda(val)
        elif mnemonic == "LDB":
            self.ldb(val)
        elif mnemonic == "LDL":
            self.ldl(val)
        elif mnemonic == "LDS":
            self.lds(val)
        elif mnemonic == "LDT":
            self.ldt(val)
        elif mnemonic == "LDX":
            self.ldx(val)
        elif mnemonic == "MUL":
            self.mul(val)
        elif mnemonic == "RD":
            self.rd(val)
        elif mnemonic == "RSUB":
            self.rsub()
        elif mnemonic == "STA":
            self.sta(addr)
        elif mnemonic == "STB":
            self.stb(addr)
        elif mnemonic == "STL":
            self.stl(addr)
        elif mnemonic == "STS":
            self.sts(addr)
        elif mnemonic == "STSW":
            self.stsw(addr)
        elif mnemonic == "STT":
            self.stt(addr)
        elif mnemonic == "STX":
            self.stx(addr)
        elif mnemonic == "SUB":
            self.sub(val)
        elif mnemonic == "TD":
            self.td(val)
        elif mnemonic == "WD":
            self.wd(val)
        else:
            self.not_implemented(mnemonic)
            return False
        return True

    # FUNCTIONS - FORMAT 1
    def fix(self):
        f = self.get_f()
        self.set_a(int(f))

    def float(self):
        a = self.get_a()
        self.set_f(float(a))

    # FUNCTIONS - FORMAT 2
    # r1, r2 indeksa v tabeli regs
    def add_r(self, r1, r2):
        r1_val = self.get_reg(r1)
        r2_val = self.get_reg(r2)
        self.set_reg(r2, r1_val + r2_val)

    def comp_r(self, r1, r2):
        r1_val = self.get_reg(r1)
        r2_val = self.get_reg(r2)
        # Za register SW nas zanimata le bita CC:
        # 0x00 - manjse
        # 0x40 - enako
        # 0x80 - vecje
        if r1_val < r2_val:
            self.set_sw(0x00)
        elif r1_val == r2_val:
            self.set_sw(0x40)
        else:
            self.set_sw(0x80)

    def div_r(self, r1, r2):
        r1_val = self.get_reg(r1)
        r2_val = self.get_reg(r2)
        self.set_reg(r2, r2_val / r1_val)

    def mul_r(self, r1, r2):
        r1_val = self.get_reg(r1)
        r2_val = self.get_reg(r2)
        self.set_reg(r2, r2_val * r1_val)

    def rmo(self, r1, r2):
        r1_val = self.get_reg(r1)
        self.set_reg(r2, r1_val)

    def sub_r(self, r1, r2):
        r1_val = self.get_reg(r1)
        r2_val = self.get_reg(r2)
        self.set_reg(r2, r2_val - r1_val)

    # FUNCTIONS - FORMAT 3/4
    def add(self, val):
        a = self.get_a()
        self.set_a(a + val)

    def sic_and(self, val):
        a = self.get_a()
        self.set_a(a & val)

    def comp(self, val):
        a = self.get_a()
        # 0x00 - manjse
        # 0x40 - enako
        # 0x80 - vecje
        if a < val:
            self.set_sw(0x00)
        elif a == val:
            self.set_sw(0x40)
        else:
            self.set_sw(0x80)

    def div(self, val):
        a = self.get_a()
        self.set_a(a // val)

    def jump(self, addr):
        self.set_pc(addr)

    def jeq(self, addr):
        if self.get_sw() == 0x40:
            self.set_pc(addr)

    def jgt(self, addr):
        if self.get_sw() == 0x80:
            self.set_pc(addr)

    def jlt(self, addr):
        if self.get_sw() == 0x00:
            self.set_pc(addr)

    def jsub(self, addr):
        pc_val = self.get_pc()
        self.set_l(pc_val)
        self.set_pc(addr)

    def lda(self, val):
        self.set_a(val)

    def ldb(self, val):
        self.set_b(val)

    def ldl(self, val):
        self.set_l(val)

    def lds(self, val):
        self.set_s(val)

    def ldt(self, val):
        self.set_t(val)

    def ldx(self, val):
        self.set_x(val)

    def mul(self, val):
        a = self.get_a()
        self.set_a(a * val)

    def sic_or(self, val):
        a = self.get_a()
        self.set_a(a | val)

    def rd(self, val):
        self.set_a(self.devices[val].read())

    def rsub(self):
        l = self.get_l()
        self.set_pc(l)

    def sta(self, addr):
        a = self.get_a()
        self.set_word(addr, a)


    def stb(self, addr):
        b = self.get_b()
        self.set_word(addr, b)

    def stl(self, addr):
        l = self.get_l()
        self.set_word(addr, l)

    def sts(self, addr):
        s = self.get_s()
        self.set_word(addr, s)

    def stsw(self, addr):
        sw = self.get_sw()
        self.set_word(addr, sw)

    def stt(self, addr):
        t = self.get_t()
        self.set_word(addr, t)

    def stx(self, addr):
        x = self.get_x()
        self.set_word(addr, x)

    def sub(self, val):
        a = self.get_a()
        self.set_a(a - val)

    def td(self, val):
        device = self.devices[val]
        device.test()

    def wd(self, val):
        device = self.devices[val]
        a = self.get_a() & 0xFF # rightmost byte
        device.write(a)


    # DOSTOP DO NAPRAV
    def get_device(self, num: int) -> Optional[Device]:
        if not 0 <= num < 256:
            raise ValueError("Device number must be 0-255")
        return self.devices[num]

    # Sets a FileDevice
    # Doesn't allow overwriting of the standard devices
    def set_device(self, num: int):
        if not 2 < num < 256:
            raise ValueError("Device number must be 3-255")
        self.devices[num] = FileDevice(num)

    # NALAGANJE
    def load_section(self, reader):

        while True:
            rec_type = reader.read(1)
            if not rec_type:
                print(self.memory)
                break

            if rec_type == 'H':
                Utils.read_string(reader, 6) # name
                Utils.read_word(reader) # start_addr
                Utils.read_word(reader) # length
                # konec vrstice
                reader.readline()

            elif rec_type == 'T':
                addr = Utils.read_word(reader)
                size = Utils.read_byte(reader)
                for i in range(size):
                    byte = Utils.read_byte(reader)
                    self.set_byte(addr + i, byte)
                reader.readline()

            elif rec_type == 'E':
                exec_addr = Utils.read_word(reader)
                self.set_pc(exec_addr)
                reader.readline()
                return True

            else:
                raise ValueError(f"Unknown record type {rec_type}")

        return False

    # ERROR HANDLING
    def not_implemented(self, mnemonic: str):
        msg = "[ERROR]" + mnemonic + " is not implemented.\n"
        for b in msg.encode('utf-8'):
            self.devices[2].write(b)

    def invalid_opcode(self, opcode: int):
        msg = "[ERROR]" + f'0x{opcode:02X}' + ' is invalid.\n'
        for b in msg.encode('utf-8'):
            self.devices[2].write(b)

    def invalid_addressing(self):
        msg = "[ERROR]" + "Invalid addressing.\n"
        for b in msg.encode('utf-8'):
            self.devices[2].write(b)

    def unknown_error(self):
        msg = "[ERROR]" + "Unknown error.\n"
        for b in msg.encode('utf-8'):
            self.devices[2].write(b)

    def unexpected_eof(self):
        msg = "[ERROR]" + "Unexpected EOF\n"
        for b in msg.encode('utf-8'):
            self.devices[2].write(b)

    # DISASSEMBLER
    def disassemble(self, addr: int):
        try:
            opcode_byte = self.memory[addr]
            opcode = opcode_byte & 0xFC

            op = Opcode()
            sic_format = op.get_format(opcode)
            mnemonic = op.get_mnemonic(opcode)

            if sic_format == -1:
                return (-1, f"{addr:06X}: ??")

            # FORMAT 1
            if sic_format == 1:
                return (1, f"{addr:06X}: {mnemonic}")

            # FORMAT 2
            if sic_format == 2:
                byte2 = self.memory[addr+1]
                r1 = (byte2 >> 4) & 0xF
                r2 = byte2 & 0xF
                return (2, f"{addr:06X}: {mnemonic} {r1}, {r2}")

            # FORMAT 3/4
            byte2 = self.memory[addr+1]
            byte3 = self.memory[addr+2]

            e = (byte2 >> 4) & 1
            disp = ((byte2 & 0x0F) << 8) | byte3

            if e:
                # FORMAT 4
                byte4 = self.memory[addr+3]
                addr_val = (disp << 8) | byte4
                return (4, f"{addr:06X}: +{mnemonic} {addr_val:05X}")
            else:
                # FORMAT 3
                return (3, f"{addr:06X}: {mnemonic} {disp:03X}")

        except Exception:
            return (-1, f"{addr:06X}: <ERR>")

