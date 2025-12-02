
import sys
from typing import List
from device import Device, InputDevice, OutputDevice

MAX_ADDRESS = 2 ** 20  # naslovni prostor (20-bitov)

class Machine:

    def __init__(self):
        # registri
        self.regs = [0] * 10 # [A, X, L, B, S, T, F, -, PC, SW]
        self.regs[6] = 0.0 # register F

        # pomnilink
        self.memory = bytearray(MAX_ADDRESS)

        # naprave
        self.devices: List[Device] = [None] * 256
        self.devices[0] = InputDevice(stream=open(0, 'rb')) # standardni vhod (read byte)
        self.devices[1] = OutputDevice(stream=open(1, 'wb')) # standardni izhod (write byte)
        self.devices[2] = OutputDevice(stream=open(2, 'wb')) # standardni izhod za napake (write byte)

        # disassembly
        dissassembly = []


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

    def getWord(self, addr, val):
        if 0 <= addr < MAX_ADDRESS - 3:
            self.memory[addr] = (val >> 16) & 0xFF # ohrani samo spodnji Byte
            self.memory[addr + 1] = (val >> 8) & 0xFF
            self.memory[addr + 2] = val & 0xFF
            return (self.memory[addr] << 16) | (self.memory[addr+1] << 8) | (self.memory[addr+2]);
        else: raise ValueError("Naslov izven meja.")

    # dostop do naprav
    def getDevice(self, num) -> Device:
        if 0 <= num < 256:
            return self.devices[num]
        else: raise ValueError("Indeks naprave izven obsega.")

    def setDevice(self, num, device):
        if 0 <= num < 256:
            self.devices[num] = device
        else: raise ValueError("Indeks naprave izven obsega.")

    # branje obj code
    def readObjCode(self, fileName):
        # read mode, po vrsticah
        with open(fileName) as file:
            lines = [line.strip() for line in file if line.strip()]

        for line in lines:
            record_type = line[0]
            # HEADER
            if record_type == "H":
                name = line[1:7].strip()
                start = int(line[8:13], 16) #hex to 10
                #self.setPC(start)
                length = int(line[13:19], 16)

            # TEXT
            elif record_type == "T":
                t_start = int(line[1:7], 16)
                t_len = int(line[7:9], 16)
                t_data = line[9:]
                # preostanek preberemo po bytih in shranimo v pomnilnik
                for i in range(0, t_len, 2):
                    byte = int(t_data[i:i+2], 16)
                    self.setByte(t_start + i//2, byte)

            # END
            elif record_type == "E":
                e_start = int(line[1:], 16)
                self.setPC(e_start)

        def step(self):
            instr =

        #file.read(1) # H
        #name = file.read(6)
        #start = file.read(6)
        #self.setPC(start)



