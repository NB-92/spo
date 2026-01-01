
import sys
from typing import List
from device import Device, InputDevice, OutputDevice, FileDevice

MAX_ADDRESS = 2 ** 20  # naslovni prostor (20-bitov)

class Machine:

    def __init__(self):
        # POMNILNIK
        self.memory = bytearray(MAX_ADDRESS)

        # REGISTRI
        self.reset()

        # NAPRAVE
        # SIC/XE podpira 256 naprav
        self.devices: List[Device] = [None] * 256

        # Standardni vhod, izhod in izhod za napake
        self.devices[0] = InputDevice(open(0, 'rb'))
        self.devices[1] = OutputDevice(open(1, 'wb'))
        self.devices[2] = OutputDevice(open(2, 'wb'))


    def reset(self):
        self.regs = [0] * 10 # [A, X, L, B, S, T, F, -, PC, SW]
        # Za register SW nas zanimata le bita CC:
        # 0x00 - manjse
        # 0x40 - enako
        # 0x80 - vecje
        self.regs[6] = 0.0 # register F bo float

    # dostop do registrov
    def getA(self) -> int: return self.regs[0]
    def setA(self, val): self.regs[0] = val

    def getX(self) -> int: return self.regs[1]
    def setX(self, val): self.regs[1] = val

    def getL(self) -> int: return self.regs[2]
    def setL(self, val): self.regs[2] = val

    def getB(self) -> int: return self.regs[3]
    def setB(self, val): self.regs[3] = val

    def getS(self) -> int: return self.regs[4]
    def setS(self, val): self.regs[4] = val

    def getT(self) -> int: return self.regs[5]
    def setT(self, val): self.regs[5] = val

    def getF(self) -> int: return self.regs[6]
    def setF(self, val): self.regs[6] = val

    def getPC(self) -> int: return self.regs[8]
    def setPC(self, val): self.regs[8] = val

    def getSW(self) -> int: return self.regs[9]
    def setSW(self, val): self.regs[9] = val

    # dostop do vrednosti po indeksu
    def getReg(self, index) -> int: return self.regs[index]
    def setReg(self, index, val):
        if index == 6:
            self.regs[6] = float(val)
        else: self.regs[index] = val

    #dostop do pomnilnika:
    def getByte(self, addr):
        if 0 <= addr < MAX_ADDRESS:
            return self.memory[addr]
        else: raise ValueError("Naslov izven meja.")

    def setByte(self, addr, val):
        if 0 <= addr < MAX_ADDRESS:
            self.memory[addr] = val
        else: raise ValueError("Naslov izven meja.")

    def getWord(self, addr):
        if 0 <= addr < MAX_ADDRESS - 3:
            return (self.memory[addr] << 16) | (self.memory[addr + 1] << 8) | (self.memory[addr + 2]);
        else: raise ValueError("Naslov izven meja.")

    def setWord(self, addr, val):
        if 0 <= addr < MAX_ADDRESS - 3:
            self.memory[addr] = (val >> 16) & 0xFF # ohrani samo spodnji Byte
            self.memory[addr + 1] = (val >> 8) & 0xFF
            self.memory[addr + 2] = val & 0xFF
            return (self.memory[addr] << 16) | (self.memory[addr+1] << 8) | (self.memory[addr+2]);
        else: raise ValueError("Naslov izven meja.")

    # DOSTOP DO NAPRAV
    def getDevice(self, num: int) -> Device:
        if not 0 <= num < 256:
            raise ValueError("Device number must be 0-255")
        return self.devices[num]

    # Sets a FileDevice
    # Doesn't allow overwriting of the standard devices
    def set_device(self, num: int):
        if not 2 < num < 256:
            raise ValueError("Device number must be 3-255")
        self.devices[num] = FileDevice(num);