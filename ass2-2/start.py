

if __name__ == "__main__":
    from machine import Machine

    m = Machine()

    # Load a simple format 3 instruction into memory: LDA (0x00)
    # LDA format 3: opcode 0x00 + 2 bytes operand
    m.set_byte(0, 0x00)  # opcode byte
    m.set_byte(1, 0x10)  # operand high byte
    m.set_byte(2, 0x20)  # operand low byte

    # Set program counter to start of program
    m.set_pc(0)

    # Execute one instruction
    m.execute()