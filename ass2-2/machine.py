
from typing import List
from device import Device, InputDevice, OutputDevice

MAX_ADDRESS = 2 ** 20  # naslovni prostor (20-bitov)

class Machine:

    def __init__(self):
        # registri
        self.regs = [0] * 10 # [A, X, L, B, S, T, F, -, PC, SW]
        self.regs[6] = 0.0 # register F

        #pomnilink
        self.memory = bytearray(MAX_ADDRESS)

        #naprave
        self.devices: List[Device] = [None] * 256
        self.devices[0] = InputDevice(stream=open(0, 'rb')) # standardni vhod (read byte)
        self.devices[1] = OutputDevice(stream=open(1, 'wb')) # standardni izhod (write byte)
        self.devices[2] = OutputDevice(stream=open(2, 'wb')) # standardni izhod za napake (write byte)


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
    def setF(self, val): self.regs[8] = val

    def getSW(self) -> int: return self.regs[9]
    def setF(self, val): self.regs[9] = val

    # dostop do vrednosti po indeksu
    def getReg(self, index) -> int: return self.regs[index]
    def setF(self, index, val):
        if index == 6:
            self.regs[6] = float(val)
        else: self.regs[index] = val

    #dostop do pomnilnika:
    def getByte(self, addr):
        if 0 <= addr < MAX_ADDRESS:
            return self.memory[addr]
        raise ValueError("Naslov izven meja.")

    def setByte(self, addr, val):
        if 0 <= addr < MAX_ADDRESS:
            self.memory[addr] = val
        raise ValueError("Naslov izven meja.")

    def getWord(self, addr):
        if 0 <= addr < MAX_ADDRESS - 3:
            return (self.memory[addr] << 16) | (self.memory[addr + 1] << 8) | (self.memory[addr + 2]);
        raise ValueError("Naslov izven meja.")

    def getWord(self, addr, val):
        if 0 <= addr < MAX_ADDRESS - 3:
            self.memory[addr] = (val >> 16) & 0xFF # ohrani samo spodnji Byte
            self.memory[addr + 1] = (val >> 8) & 0xFF
            self.memory[addr + 2] = val & 0xFF
            return (self.memory[addr] << 16) | (self.memory[addr+1] << 8) | (self.memory[addr+2]);
        raise ValueError("Naslov izven meja.")

    # dostop do naprav
    def getDevice(self, num) -> Device:
        if 0 <= num < 256:
            return self.devices[num]
        raise ValueError("Indeks naprave izven obsega.")

    def setDevice(self, num, device):
        if 0 <= num < 256:
            self.devices[num] = device
        raise ValueError("Indeks naprave izven obsega.")





