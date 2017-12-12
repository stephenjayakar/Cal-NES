class CPU:
    # Random Access Memory
    ram = 0
    # Program Counter
    PC = 0
    # Processor Status
    P = 0b0
    # Stack Pointer ($0100-$01FF)
    SP = 0
    
    # Registers
    reg = {}

    opcode_to_instruction = {}

    def __init__(self, ram, PC_START = 0x8000, SP_START = 0x200):
        self.ram = ram
        self.PC = PC_START
        self.SP = SP_START #not sure if this should be 100

        self.reg = {"A": bytearray([0]),
                    "X": bytearray([0]),
                    "Y": bytearray([0])}

        CPU.opcode_to_instruction = {0x69: self.ADC, 0x65: self.ADC, 0x75: self.ADC, 0x6D: self.ADC, 0x7D: self.ADC,
                                     0x79: self.ADC, 0x61: self.ADC, 0x71: self.ADC,
                                     0x29: self.AND, 0x25: self.AND, 0x35: self.AND, 0x2D: self.AND, 0x3D: self.AND,
                                     0x39: self.AND, 0x21: self.AND, 0x31: self.AND,
                                     0x0A: self.ASL, 0x06: self.ASL, 0x16: self.ASL, 0x0E: self.ASL, 0x1E: self.ASL,
                                     0x90: self.BCC, 0xB0: self.BCS,
                                     0xF0: self.BEQ,
                                     0x24: self.BIT, 0x2C: self.BIT,
                                     0x30: self.BMI,
                                     0xD0: self.BNE,
                                     0x10: self.BPL,
                                     0x00: self.BRK,
                                     0x50: self.BVC,
                                     0x70: self.BVS,
                                     0x18: self.CLC,
                                     0xD8: self.CLD,
                                     0x58: self.CLI,
                                     0xB8: self.CLV,
                                     0xC9: self.CMP, 0xC5: self.CMP, 0xD5: self.CMP, 0xCD: self.CMP, 0xDD: self.CMP,
                                     0xD9: self.CMP, 0xC1: self.CMP, 0xD1: self.CMP,
                                     0xE0: self.CPX, 0xE4: self.CPX, 0xEC: self.CPX,
                                     0xC0: self.CPY, 0xC4: self.CPY, 0xCC: self.CPY,
                                     0xC6: self.DEC, 0xD6: self.DEC, 0xCE: self.DEC, 0xDE: self.DEC,
                                     0xCA: self.DEX,
                                     0x88: self.DEY,
                                     0x49: self.EOR, 0x45: self.EOR, 0x55: self.EOR, 0x4D: self.EOR, 0x5D: self.EOR,
                                     0x59: self.EOR, 0x41: self.EOR, 0x51: self.EOR,
                                     0xE6: self.INC, 0xF6: self.INC, 0xEE: self.INC, 0xFE: self.INC,
                                     0xE8: self.INX,
                                     0xC8: self.INY,
                                     0x4C: self.JMP, 0x6C: self.JMP,
                                     0x20: self.JSR,
                                     0xA9: self.LDA, 0xA5: self.LDA, 0xB5: self.LDA, 0xAD: self.LDA, 0xBD: self.LDA,
                                     0xB9: self.LDA, 0xA1: self.LDA, 0xB1: self.LDA,
                                     0xA2: self.LDX, 0xA6: self.LDX, 0xB6: self.LDX, 0xAE: self.LDX, 0xBE: self.LDX,
                                     0xA0: self.LDY, 0xA4: self.LDY, 0xB4: self.LDY, 0xAC: self.LDY, 0xBC: self.LDY,
                                     0x4A: self.LSR, 0x46: self.LSR, 0x56: self.LSR, 0x4E: self.LSR, 0x5E: self.LSR,
                                     0xEA: self.NOP,
                                     0x09: self.ORA, 0x05: self.ORA, 0x15: self.ORA, 0x0D: self.ORA, 0x1D: self.ORA,
                                     0x19: self.ORA, 0x01: self.ORA, 0x11: self.ORA,
                                     0x48: self.PHA,
                                     0x08: self.PHP,
                                     0x68: self.PLA,
                                     0x28: self.PLP,
                                     0x2A: self.ROL, 0x26: self.ROL, 0x36: self.ROL, 0x2E: self.ROL, 0x3E: self.ROL,
                                     0x6A: self.ROR, 0x66: self.ROR, 0x76: self.ROR, 0x6E: self.ROR, 0x7E: self.ROR,
                                     0x40: self.RTI,
                                     0x60: self.RTS,
                                     0xE9: self.SBC, 0xE5: self.SBC, 0xF5: self.SBC, 0xED: self.SBC, 0xFD: self.SBC,
                                     0xF9: self.SBC, 0xE1: self.SBC, 0xF1: self.SBC,
                                     0x38: self.SEC,
                                     0xF8: self.SED,
                                     0x78: self.SEI,
                                     0x85: self.STA, 0x95: self.STA, 0x8D: self.STA, 0x9D: self.STA, 0x99: self.STA,
                                     0x81: self.STA, 0x91: self.STA,
                                     0x86: self.STX, 0x96: self.STX, 0x8E: self.STX,
                                     0x84: self.STY, 0x94: self.STY, 0x8C: self.STY,
                                     0xAA: self.TAX,
                                     0xA8: self.TAY,
                                     0xBA: self.TSX,
                                     0x8A: self.TXA,
                                     0x9A: self.TXS,
                                     0x98: self.TYA
                                    }


    def run_instruction(self):
        opcode = self.get_PC_byte()
        if opcode not in CPU.opcode_to_instruction:
            return self.invalid_instruction(opcode)
        f = CPU.opcode_to_instruction[opcode]
        print("opcode: " + hex(opcode))
        print("instruction: " + str(f))
        # Do we actually need the output?
        res = f(opcode)

    def tick(self):
        self.run_instruction()
        
    def run_all(self):
        for i in range(10):
            print(self._cpu_dump())
            self.run_instruction()


    def get_mem(self, addr):
        return self.ram.mem_get(addr, 1)[0]

    def set_mem(self, addr, byte):
        self.ram.mem_set(addr, bytearray([byte]))

    def get_PC_byte(self):
        byte = self.get_mem(self.PC)
        self.PC += 1
        return byte


    def get_zero_page_addr(self, offset=0):
        return self.get_PC_byte() + offset

    def get_zero_page_addr_x(self):
        return self.get_zero_page_addr(self.X)

    def get_zero_page_addr_y(self):
        return self.get_zero_page_addr(self.Y)


    def get_zero_page(self, offset=0):
        addr = self.get_PC_byte() + offset
        mem_byte = self.get_mem(addr)
        return mem_byte

    def get_zero_page_x(self):
        return self.get_zero_page(self.X)

    def get_zero_page_y(self):
        return self.get_zero_page(self.Y)


    def get_absolute_addr(self, offset=0):
        lower = self.get_PC_byte()
        upper = self.get_PC_byte()
        return (upper << 8 | lower) + offset

    def get_absolute_addr_x(self):
        return self.get_absolute_addr(self.X)

    def get_absolute_addr_y(self):
        return self.get_absolute_addr(self.Y)


    def get_absolute(self, offset=0):
        lower = self.get_PC_byte()
        upper = self.get_PC_byte()
        addr = (upper << 8 | lower) + offset
        mem_byte = self.get_mem(addr)
        return mem_byte

    def get_absolute_x(self):
        return self.get_absolute(self.X)

    def get_absolute_y(self):
        return self.get_absolute(self.Y)

    # This probably works
    def get_relative_addr(self):
        offset = self.convert_8bit_twos(self.get_PC_byte())
        addr = self.PC + offset
        return addr

    # TODO: Do a proof of correctness on the value returned lol
    def get_indirect_addr(self, reg_offset=0):
        # The next byte after opcode
        zero_page_addr = self.get_PC_byte()
        addr = self.get_mem(zero_page_addr) + (self.get_mem(zero_page_addr + 1) << 8)
        return addr + reg_offset
        # addr = offset + reg_offset
        # lower = self.get_mem(addr)
        # upper = self.get_mem(addr + 1)
        # return (upper << 8) + lower

    def get_indirect_addr_x(self):
        return self.get_indirect_addr(self.X)

    def get_indirect_addr_y(self):
        return self.get_indirect_addr(self.Y)


    def get_indirect(self, offset=0):
        addr = self.get_absolute_addr(offset)
        lower = self.get_mem(addr)
        upper = self.get_mem(addr + 1)
        real_addr = (upper << 8) + lower
        return self.get_mem(real_addr)

    def get_indirect_x(self):
        return self.get_indirect(self.X)

    def get_indirect_y(self):
        return self.get_indirect(self.Y)


    def ADC(self, opcode):
        # ***** ADC(ADd with Carry) *****
        if opcode == 0x69: #Immediate, 2, 2
            operand = self.get_PC_byte();
        elif opcode == 0x65: #Zero Page, 2, 3
            operand = self.get_zero_page_x()
        elif opcode == 0x75: #Zero Page,X, 2, 4
            operand = self.get_zero_page_x()
        elif opcode == 0x6D: #Absolute, 3, 4
            operand = self.get_absolute()
        elif opcode == 0x7D: #Absolute,X, 3, 4
            operand = self.get_absolute_x()
        elif opcode == 0x79: #Absolute,Y, 3, 4
            operand = self.get_absolute_y()
        elif opcode == 0x61: #(Indirect,X) 2, 6
            operand = self.get_indirect_x()
        elif opcode == 0x71: #(Indirect,Y) 2, 5
            operand = self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        result = self.A + operand + self.C()
        self.A = result & 0xFF

        self.set_C(result >> 8)
        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)


    def AND(self, opcode):
        #***** AND - Logical AND *****
        if opcode == 0x29: #Immediate, 2, 2
            self.A = self.A & self.get_PC_byte()
        elif opcode == 0x25: #Zero Page, 2, 3
            self.A = self.A & self.get_zero_page()
        elif opcode == 0x35: #Zero Page,X, 2, 4
            self.A = self.A & self.get_zero_page_x()
        elif opcode == 0x2D: #Absolute, 3, 4
            self.A = self.A & self.get_absolute()
        elif opcode == 0x3D: #Absolute,X, 3, 4
            self.A = self.A & self.get_absolute_x()
        elif opcode == 0x39: #Absolute,Y, 3, 4
            self.A = self.A & self.get_absolute_y()
        elif opcode == 0x21: #(Indirect,X) 2, 6
            self.A = self.A & self.get_indirect_x()
        elif opcode == 0x31: #(Indirect,Y) 2, 5
            self.A = self.A & self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        # update processor status
        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)

    def ASL(self, opcode):
        #***** ASL - Arithmetic Shift Left: *****"""
        if opcode == 0x0A: #Accumulator, 1, 2
            operand = self.A
            result = (self.A << 1) & 0xFF
            self.A = result

        else:
            if opcode == 0x06: #Zero Page, 2, 5
                addr = self.get_zero_page_addr()
            elif opcode == 0x16: #Zero Page,X, 2, 6
                addr = self.get_zero_page_addr_x()
            elif opcode == 0x0E: #Absolute, 3, 6
                addr = self.get_absolute_addr()
            elif opcode == 0x1E: #Absolute,X, 3, 7
                addr = self.get_absolute_addr_x()
            else:
                return self.invalid_instruction(opcode)

            operand = self.get_mem(addr)
            result = (operand << 1) & 0xFF
            self.set_mem(addr, result)

        self.set_C(operand >> 7)
        self.set_Z(self.A == 0)
        self.set_N(result >> 7)

    def BCC(self, opcode):
        #***** BCC - Branch if Carry Clear *****
        addr = self.get_relative_addr()
        if opcode == 0x90:  #Relative, 2, 2
            if not self.C():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BCS(self, opcode):
        #***** BCS - Branch if Carry Set *****
        addr = self.get_relative_addr()
        if opcode == 0xB0:  #Relative, 2, 2
            if self.C():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BEQ(self, opcode):
        #***** BEQ - Branch if Equal *****
        addr = self.get_relative_addr()
        if opcode == 0xF0:  #Relative, 2, 2
            if self.Z():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BIT(self, opcode):
        #***** BIT - Bit Test *****
        if opcode == 0x24: #Zero Page, 2, 3
            operand = self.get_zero_page()
        elif opcode == 0x2C:  #Absolute, 3, 4
            operand = self.get_absolute()
        else:
            return self.invalid_instruction(opcode)

        result = self.A & operand
        self.set_Z(result == 0)
        self.set_V(self.get_bit(operand, 6))
        self.set_N(self.get_bit(operand, 7))


    def BMI(self, opcode):
        #***** BMI - Branch if Minus *****
        addr = self.get_relative_addr()
        if opcode == 0x30:  #Relative, 2, 2
            if self.N():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BNE(self, opcode):
        #***** BNE - Branch if Not Equal *****
        addr = self.get_relative_addr()
        if opcode == 0xD0:  #Relative, 2, 2
            if not self.Z():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BPL(self, opcode):
        #***** BPL - Branch if Positive *****
        addr = self.get_relative_addr()
        print(addr)
        if opcode == 0x10:  #Relative, 2, 2
            if not self.N():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BRK(self, opcode):
        #***** BRK - Force Interrupt *****
        if opcode == 0x00:  #Implied, 1, 7
            # Push PC and P on stack
            self.SP -= 3
            bytes_to_stack = bytearray([self.P, self.PC & 0xFF, self.PC >> 8])
            self.ram.mem_set(self.SP, bytes_to_stack)

            # Set PC as IRQ vector
            lower = self.get_mem(0xFFFE)
            upper = self.get_mem(0xFFFF)
            self.PC = (upper << 8) | lower

            # Set fag
            self.set_B(1)
        else:
            return self.invalid_instruction(opcode)

    def BVC(self, opcode):
        #***** BVC - Branch if OverFlow Clear *****
        addr = self.get_relative_addr()
        if opcode == 0x50:  #Relative, 2, 2
            if not self.V():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def BVS(self, opcode):
        #***** BVS - Branch if OverFlow Set *****
        addr = self.get_relative_addr()
        if opcode == 0x70:  #Relative, 2, 2
            if self.V():
                self.PC = addr
        else:
            return self.invalid_instruction(opcode)

    def CLC(self, opcode):
        #***** CLC - Clear Carry Flag *****
        if opcode == 0x18: #Implied, 1, 2
            self.set_C(0)
        else:
            return self.invalid_instruction(opcode)

    def CLD(self, opcode):
        #***** CLD - Clear Decimal Mode *****
        if opcode == 0xD8: #Implied, 1, 2
            self.set_D(0)
        else:
            return self.invalid_instruction(opcode)

    def CLI(self, opcode):
        #***** CLI - Clear Interrupt Disable *****
        if opcode == 0x58: #Implied, 1, 2
            self.set_I(0)
        else:
            return self.invalid_instruction(opcode)

    def CLV(self, opcode):
        #***** CLV - Clear Overflow Flag *****
        if opcode == 0xB8: #Implied, 1, 2
            self.set_V(0)
        else:
            return self.invalid_instruction(opcode)

    def CMP(self, opcode):
        #***** CMP - Compare *****
        if opcode == 0xC9: #Immediate 2, 2
            operand = self.get_PC_byte()
        elif opcode == 0xC5: #Zero Page 2, 3
            operand = self.get_zero_page()
        elif opcode == 0xD5: #Zero Page,X 2, 4
            operand = self.get_zero_page_x()
        elif opcode == 0xCD: #Absolute 3, 4
            operand = self.get_zero_page_y()
        elif opcode == 0xDD: #Absolute,X 3, 4
            operand = self.get_absolute_x()
        elif opcode == 0xD9: #Absolute,Y, 3, 4
            operand = self.get_absolute_y()
        elif opcode == 0xC1: #(Indirect,X), 2, 6
            operand = self.get_indirect_x()
        elif opcode == 0xD1: #(Indirect),Y, 2, 5
            operand = self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        result = self.A - operand
        self.set_C(self.A >= operand)
        self.set_Z(result == 0)
        self.set_N(result >> 7)

    def CPX(self, opcode):
        #***** CPX - Compare X Register *****
        if opcode == 0xE0: #Immediate 2, 2
            operand = self.get_PC_byte()
        elif opcode == 0xE4: #Zero Page 2, 3
            operand = self.get_zero_page()
        elif opcode == 0xEC: #Absolute, 3, 4
            operand = self.get_absolute()
        else:
            return self.invalid_instruction(opcode)

        result = self.X - operand
        self.set_C(self.X >= operand)
        self.set_Z(result == 0)
        self.set_N(result >> 7)

    def CPY(self, opcode):
        #***** CPY - Compare Y Register *****
        if opcode == 0xC0: #Immediate 2, 2
            operand = self.get_PC_byte()
        elif opcode == 0xC4: #Zero Page 2, 3
            operand = self.get_zero_page()
        elif opcode == 0xCC: #Absolute, 3, 4
            operand = self.get_absolute()
        else:
            return self.invalid_instruction(opcode)

        result = self.Y - operand
        self.set_C(self.Y >= operand)
        self.set_Z(result == 0)
        self.set_N(result >> 7)

    def DEC(self, opcode):
        #***** DEC - Decrement Memory *****
        if opcode == 0xC6: #Zero Page 2, 5
            addr = self.get_zero_page_addr()
        elif opcode == 0xD6: #Zero Page,X, 2, 6
            addr = self.get_zero_page_addr_x()
        elif opcode == 0xCE: #Absolute, 3, 6
            addr = self.get_absolute_addr()
        elif opcode == 0xDE: #Absolute,X, 3, 7
            addr = self.get_absolute_addr_x()
        else:
            return self.invalid_instruction(opcode)

        result = self.get_mem(addr) - 1
        self.set_mem(addr, result)
        self.set_Z(result == 0)
        self.set_N(result >> 7)

    def DEX(self, opcode):
        #***** DEX - Decrement X Register *****
        if opcode == 0xCA: #Implied 1, 2
            self.X = self.X - 1
            self.set_Z(self.X == 0)
            self.set_N(self.X >> 7)

        else:
            return self.invalid_instruction(opcode)

    def DEY(self, opcode):
        #***** DEY - Decrement Y Register *****
        if opcode == 0x88: #Implied 1, 2
            self.Y = self.Y - 1
            self.set_Z(self.Y == 0)
            self.set_N(self.Y >> 7)
        else:
            return self.invalid_instruction(opcode)

    def EOR(self, opcode):
        #***** EOR - Exclusive OR *****
        if opcode == 0x49:  # Immediate, 2, 2
            self.A = self.A ^ self.get_PC_byte()
        elif opcode == 0x45:  # Zero Page, 2, 3
            self.A = self.A ^ self.get_zero_page()
        elif opcode == 0x55:  # Zero Page X, 2, 4
            self.A = self.A ^ self.get_zero_page_x()
        elif opcode == 0x4D:  # Absolute, 3, 4
            self.A = self.A ^ self.get_absolute()
        elif opcode == 0x5D:  # Absolute X, 3, 4 (+1 if page crossed)
            self.A = self.A ^ self.get_absolute_x()
        elif opcode == 0x59:  # Absolute Y, 3, 4 (+1 if page crossed)
            self.A = self.A ^ self.get_absolute_y()
        elif opcode == 0x41:  # Indirect X, 2, 6
            self.A = self.A ^ self.get_indirect_x()
        elif opcode == 0x51:  # Indirect Y, 2, 5 (+1 if page crossed)
            self.A = self.A ^ self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)

    def INC(self, opcode):
        #***** INC - Increment Memory *****
        if opcode == 0xE6:  # Zero Page, 2, 5
            addr = self.get_zero_page_addr()
        elif opcode == 0xF6:  # Zero Page X, 2, 6
            addr = self.get_zero_page_addr_x()
        elif opcode == 0xEE:  # Absolute, 3, 6
            addr = self.get_absolute_addr()
        elif opcode == 0xFE:  # Absolute X, 3, 7
            addr = self.get_absolute_addr_x()
        else:
            return self.invalid_instruction(opcode)

        result = self.get_mem(addr) + 1
        self.set_mem(addr, result)
        self.set_Z(result == 0)
        self.set_N(result >> 7)

    def INX(self, opcode):
        #***** INX - Increment X Register *****
        if opcode == 0xE8:  # Implied, 1, 2
            self.X = self.X + 1
            self.set_Z(self.X == 0)
            self.set_N(self.X >> 7)
        else:
            return self.invalid_instruction(opcode)

    def INY(self, opcode):
        #***** INY - Increment Y Register *****
        if opcode == 0xC8:  # Implied, 1, 2
            self.Y = self.Y + 1
            self.set_Z(self.Y == 0)
            self.set_N(self.Y >> 7)
        else:
            return self.invalid_instruction(opcode)

    def JMP(self, opcode):
        #***** JMP - Jump *****
        if opcode == 0x4C:  # Absolute, 3, 3
            self.PC = self.get_absolute()
        elif opcode == 0x6C:  # Indirect, 3, 5
            self.PC = self.get_indirect()
        else:
            return self.invalid_instruction(opcode)

    def JSR(self, opcode):
        #***** JSR - Jump to Subroutine *****
        if opcode == 0x20:  # Absolute, 3, 6
            jump_addr = self.get_absolute_addr()
            self.SP -= 2
            bytes_to_load = bytearray([self.PC & 0xFF, self.PC >> 8])
            self.ram.mem_set(self.SP, bytes_to_load)
            self.PC = jump_addr
        else:
            return self.invalid_instruction(opcode)

    def LDA(self, opcode):
        #***** LDA - Load Accumulator *****
        if opcode == 0xA9:  # Immediate, 2, 2
            self.A = self.get_PC_byte()
        elif opcode == 0xA5:  # Zero Page, 2, 3
            self.A = self.get_zero_page()
        elif opcode == 0xB5:  # Zero Page X, 2, 4
            self.A = self.get_zero_page_x()
        elif opcode == 0xAD:  # Absolute, 3, 4
            self.A = self.get_absolute()
        elif opcode == 0xBD:  # Absolute X, 3, 4 (+1 if page crossed)
            self.A = self.get_absolute_x()
        elif opcode == 0xB9:  # Absolute Y, 3, 4 (+1 if page crossed)
            self.A = self.get_absolute_y()
        elif opcode == 0xA1:  # Indirect X, 2, 6
            self.A = self.get_indirect_x()
        elif opcode == 0xB1:  # Indirect Y, 2, 5 (+1 if page crossed)
            self.A = self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)

    def LDX(self, opcode):
        #***** LDX - Load X Register *****
        if opcode == 0xA2:  # Immediate, 2, 2
            self.X = self.get_PC_byte()
        elif opcode == 0xA6:  # Zero Page, 2, 3
            self.X = self.get_zero_page()
        elif opcode == 0xB6:  # Zero Page X, 2, 4
            self.X = self.get_zero_page_x()
        elif opcode == 0xAE:  # Absolute, 3, 4
            self.X = self.get_absolute()
        elif opcode == 0xBE:  # Absolute X, 3, 4 (+1 if page crossed)
            self.X = self.get_absolute_x()
        else:
            return self.invalid_instruction(opcode)

        self.set_Z(self.X == 0)
        self.set_N(self.X >> 7)

    def LDY(self, opcode):
        #***** LDY - Load Y Register *****
        if opcode == 0xA0:  # Immediate, 2, 2
            self.Y = self.get_PC_byte()
        elif opcode == 0xA4:  # Zero Page, 2, 3
            self.Y = self.get_zero_page()
        elif opcode == 0xB4:  # Zero Page X, 2, 4
            self.Y = self.get_zero_page_x()
        elif opcode == 0xAC:  # Absolute, 3, 4
            self.Y = self.get_absolute()
        elif opcode == 0xBC:  # Absolute X, 3, 4 (+1 if page crossed)
            self.Y = self.get_absolute_x()
        else:
            return self.invalid_instruction(opcode)

        self.set_Z(self.Y == 0)
        self.set_N(self.Y >> 7)

    def LSR(self, opcode):
        # ***** LSR - Logical Shift Right *****
        if opcode == 0x4A: #Accumulator, 1, 2
            operand = self.A
            result = self.A >> 1
            self.A = result

        else:
            if opcode == 0x46: #Zero Page, 2, 5
                addr = self.get_zero_page_addr()
            elif opcode == 0x56: #Zero Page,X, 2, 6
                addr = self.get_zero_page_addr_x()
            elif opcode == 0x4E: #Absolute, 3, 6
                addr = self.get_absolute_addr()
            elif opcode == 0x5E: #Absolute,X, 3, 7
                addr = self.get_absolute_addr_x()
            else:
                return self.invalid_instruction(opcode)

            operand = self.get_mem(addr)
            result = operand >> 1
            self.set_mem(addr, result)

        self.set_C(operand & 0b1)
        self.set_Z(result == 0)
        self.set_N(result >> 7)


    def NOP(self, opcode):
        # ***** NOP - No Operation *****
        if opcode == 0xEA:  # Implied, 1, 2
            pass
        else:
            return self.invalid_instruction(opcode)

    def ORA(self, opcode):
        #***** ORA - Logical Inclusive OR *****
        if opcode == 0x09:  # Immediate, 2, 2
            operand = self.get_PC_byte()
        elif opcode == 0x05:  # Zero Page, 2, 3
            operand = self.get_zero_page()
        elif opcode == 0x15:  # Zero Page X, 2, 4
            operand = self.get_zero_page_x()
        elif opcode == 0x0D:  # Absolute, 3, 4
            operand = self.get_absolute()
        elif opcode == 0x1D:  # Absolute X, 3, 4 (+1 if page crossed)
            operand = self.get_absolute_x()
        elif opcode == 0x19:  # Absolute Y, 3, 4 (+1 if page crossed)
            operand = self.get_absolute_y()
        elif opcode == 0x01:  # Indirect X, 2, 6
            operand = self.get_indirect_x()
        elif opcode == 0x11:  # Indirect Y, 2, 5 (+1 if page crossed)
            operand = self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        self.A = self.A | operand
        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)

    def PHA(self, opcode):
        #***** PHA - Push Accumulator *****
        if opcode == 0x48:  # Implied, 1, 3
            self.SP -= 1
            self.set_mem(self.SP, self.A)
        else:
            return self.invalid_instruction(opcode)

    def PHP(self, opcode):
        #***** PHP - Push Processor Status *****
        if opcode == 0x08:  # Implied, 1, 3
            self.SP -= 1
            self.set_mem(self.SP, self.P)
        else:
            return self.invalid_instruction(opcode)

    def PLA(self, opcode):
        #***** PLA - Pull Accumulator *****
        if opcode == 0x68:  # Implied, 1, 4
            self.A = self.get_mem(self.SP)
            self.SP += 1
            self.set_Z(self.A == 0)
            self.set_N(self.A >> 7)
        else:
            return self.invalid_instruction(opcode)

    def PLP(self, opcode):
        #***** PLP - Pull Processor Status *****
        if opcode == 0x28:  # Implied, 1, 4
            self.P = self.get_mem(self.SP)
            self.SP += 1
        else:
            return self.invalid_instruction(opcode)

    def ROL(self, opcode):
        #***** ROL - Rotate Left *****
        if opcode == 0x2A:  # Accumulator, 1, 2
            operand = self.A
            result = (operand << 1) | self.C()
            self.A = result
        else:
            if opcode == 0x26:  # Zero Page, 2, 5
                addr = self.get_zero_page_addr()
            elif opcode == 0x36:  # Zero Page X, 2, 6
                addr = self.get_zero_page_addr_x()
            elif opcode == 0x2E:  # Absolute, 3, 6
                addr = self.get_absolute_addr()
            elif opcode == 0x3E:  # Absolute X, 3, 7
                addr = self.get_absolute_addr_x()
            else:
                return self.invalid_instruction(opcode)

            operand = self.get_mem(addr)
            result = (operand << 1) | self.C()
            self.set_mem(addr, result)

        self.set_C(operand >> 7)
        self.set_Z(self.A == 0)
        self.set_N(result >> 7)

    def ROR(self, opcode):
        #***** ROR - Rotate Right *****
        if opcode == 0x6A:  # Accumulator, 1, 2
            operand = self.A
            result = (operand >> 1) | (self.C() << 7)
            self.A = result
        else:
            if opcode == 0x66:  # Zero Page, 2, 5
                addr = self.get_zero_page_addr()
            elif opcode == 0x76:  # Zero Page X, 2, 6
                addr = self.get_zero_page_addr_x()
            elif opcode == 0x6E:  # Absolute, 3, 6
                addr = self.get_absolute_addr()
            elif opcode == 0x7E:  # Absolute X, 3, 7
                addr = self.get_absolute_addr_x()
            else:
                return self.invalid_instruction(opcode)

            operand = self.get_mem(addr)
            result = (operand >> 1) | (self.C() << 7)
            self.set_mem(addr, result)

        self.set_C(operand & 0b1)
        self.set_Z(self.A == 0)
        self.set_N(result >> 7)

    def RTI(self, opcode):
        #***** RTI - Return from Interrupt *****
        if opcode == 0x40:  # Implied, 1, 6
            loaded = self.ram.mem_get(self.SP, 3)
            self.P = loaded[0]
            lower = loaded[1]
            upper = loaded[2]
            self.PC = (upper << 8) | lower
            self.SP += 3
        else:
            return self.invalid_instruction(opcode)

    def RTS(self, opcode):
        #***** RTS - Return from Subroutine *****
        if opcode == 0x60:  # Implied, 1, 6
            loaded = self.ram.mem_get(self.SP, 2)
            lower = loaded[0]
            upper = loaded[1]
            self.PC = (upper << 8) | lower
            self.SP += 2
        else:
            return self.invalid_instruction(opcode)

    def SBC(self, opcode):
        #***** SBC - Subtract with Carry *****
        if opcode == 0xE9:  # Immediate, 2, 2
            operand = self.get_PC_byte();
        elif opcode == 0xE5:  # Zero Page, 2, 3
            operand = self.get_zero_page_x()
        elif opcode == 0xF5:  # Zero Page X, 2, 4
            operand = self.get_zero_page_x()
        elif opcode == 0xED:  # Absolute, 3, 4
            operand = self.get_absolute()
        elif opcode == 0xFD:  # Absolute X, 3, 4 (+1 if page crossed)
            operand = self.get_absolute_x()
        elif opcode == 0xF9:  # Absolute Y, 3, 4 (+1 if page crossed)
            operand = self.get_absolute_y()
        elif opcode == 0xE1:  # Indirect X, 2, 6
            operand = self.get_indirect_x()
        elif opcode == 0xF1:  # Indirect Y, 2, 5 (+1 if page crossed)
            operand = self.get_indirect_y()
        else:
            return self.invalid_instruction(opcode)

        old_A = self.A
        result = self.A - operand - (1 - self.C())
        self.A = result & 0xFF

        self.set_C(1 - (result >> 8))
        self.set_Z(self.A == 0)
        self.set_N(self.A >> 7)

        if (old_A >> 7 != operand >> 7) and (self.A >> 7 != old_A >> 7):
            self.set_V(1)
        else:
            self.set_V(0)

    def SEC(self, opcode):
        #***** SEC - Set Carry Flag *****
        if opcode == 0x38:  # Implied, 1, 2
            self.set_C(1)
        else:
            return self.invalid_instruction(opcode)

    def SED(self, opcode):
        #***** SED - Set Decimal Flag *****
        if opcode == 0xF8:  # Implied, 1, 2
            self.set_D(1)
        else:
            return self.invalid_instruction(opcode)

    def SEI(self, opcode):
        #***** SEI - Set Interrupt Disable *****
        if opcode == 0x78:  # Implied, 1, 2
            self.set_I(1)
        else:
            return self.invalid_instruction(opcode)

    def STA(self, opcode):
        #***** STA - Store Accumulator *****
        if opcode == 0x85:  # Zero Page, 2, 3
            addr = self.get_zero_page_addr()
        elif opcode == 0x95:  # Zero Page X, 2, 4
            addr = self.get_zero_page_addr_x()
        elif opcode == 0x8D:  # Absolute, 3, 4
            addr = self.get_absolute_addr()
        elif opcode == 0x9D:  # Absolute X, 3, 5
            addr = self.get_absolute_addr_x()
        elif opcode == 0x99:  # Absolute Y, 3, 5
            addr = self.get_absolute_addr_y()
        elif opcode == 0x81:  # Indirect X, 2, 6
            addr = self.get_indirect_addr_x()
        elif opcode == 0x91:  # Indirect Y, 2, 6
            addr = self.get_indirect_addr_y()
        else:
            return self.invalid_instruction(opcode)

        self.set_mem(addr, self.A)

    def STX(self, opcode):
        #***** STX - Store X Register *****
        if opcode == 0x86:  # Zero Page, 2, 3
            addr = self.get_zero_page_addr()
        elif opcode == 0x96:  # Zero Page Y, 2, 4
            addr = self.get_zero_page_addr_y()
        elif opcode == 0x8E:  # Absolute, 3, 4
            addr = self.get_absolute_addr()
        else:
            return self.invalid_instruction(opcode)

        self.set_mem(addr, self.X)

    def STY(self, opcode):
        #***** STY - Store Y Register *****
        if opcode == 0x84:  # Zero Page, 2, 3
            addr = self.get_zero_page_addr()
        elif opcode == 0x94:  # Zero Page X, 2, 4
            addr = self.get_zero_page_addr_x()
        elif opcode == 0x8C:  # Absolute, 3, 4
            addr = self.get_absolute_addr()
        else:
            return self.invalid_instruction(opcode)

        self.set_mem(addr, self.Y)

    def TAX(self, opcode):
        #***** TAX - Transfer Accumulator to X *****
        if opcode == 0xAA:  # Implied, 1, 2
            self.X = self.A
            self.set_Z(self.X == 0)
            self.set_N(self.X >> 7)
        else:
            return self.invalid_instruction(opcode)

    def TAY(self, opcode):
        #***** TAY - Transfer Accumulator to Y *****
        if opcode == 0xA8:  # Implied, 1, 2
            self.Y = self.A
            self.set_Z(self.Y == 0)
            self.set_N(self.Y >> 7)
        else:
            return self.invalid_instruction(opcode)

    def TSX(self, opcode):
        #***** TSX - Transfer Stack Pointer to X *****
        if opcode == 0xBA:  # Implied, 1, 2
            self.X = self.SP
            self.set_Z(self.X == 0)
            self.set_N(self.X >> 7)
        else:
            return self.invalid_instruction(opcode)

    def TXA(self, opcode):
        #***** TXA - Transfer X to Accumulator *****
        if opcode == 0x8A:  # Implied, 1, 2
            self.A = self.X
            self.set_Z(self.A == 0)
            self.set_N(self.A >> 7)
        else:
            return self.invalid_instruction(opcode)

    def TXS(self, opcode):
        #***** TXS - Transfer X to Stack Pointer *****
        if opcode == 0x9A:  # Implied, 1, 2
            self.SP = self.X
        else:
            return self.invalid_instruction(opcode)

    def TYA(self, opcode):
        #***** TYA - Transfer Y to Accumulator *****
        if opcode == 0x98:  # Implied, 1, 2
            self.A = self.Y
            self.set_Z(self.A == 0)
            self.set_N(self.A >> 7)
        else:
            return self.invalid_instruction(opcode)


    def invalid_instruction(self, opcode):
        print("Invalid instruction: " + hex(opcode))
        raise Exception


    def C(self):
        return self.get_bit_P(0)

    def Z(self):
        return self.get_bit_P(1)

    def I(self):
        return self.get_bit_P(2)

    def D(self):
        return self.get_bit_P(3)

    def B(self):
        return self.get_bit_P(4)

    def V(self):
        return self.get_bit_P(5)

    def N(self):
        return self.get_bit_P(6)

    def set_C(self, bit):
        self.set_bit_P(0, bit)

    def set_Z(self, bit):
        self.set_bit_P(1, bit)

    def set_I(self, bit):
        self.set_bit_P(2, bit)

    def set_D(self, bit):
        self.set_bit_P(3, bit)

    def set_B(self, bit):
        self.set_bit_P(4, bit)

    def set_V(self, bit):
        self.set_bit_P(5, bit)

    def set_N(self, bit):
        self.set_bit_P(6, bit)


    def set_bit_P(self, pos, bit):
        mask = ~(1 << pos)
        self.P = self.P & mask | (bit << pos)

    def get_bit_P(self, pos):
        return self.get_bit(self.P, pos)

    def get_bit(self, target, pos):
        return (target >> pos) & 0b1

    def convert_8bit_twos(self, num):
        if (num & (1 << 7)):
            return -((num ^ 0xFF) + 1)
        else:
            return num


    # Prints contents of registers
    def _cpu_dump(self) -> str:
        return "PC: " + str(self.PC) + "\n" + "Reg: " + str(self.reg) + "\n" + "Processor Status: " + bin(self.P)
    
    def __str__(self) -> str:
        return self._cpu_dump()


    @property
    def A(self) -> bytes:
        return self.reg["A"][0]

    @A.setter
    def A(self, value) -> None:
        self.reg["A"][0] = value % 256

    @property
    def X(self) -> bytes:
        return self.reg["X"][0]

    @X.setter
    def X(self, value) -> None:
        self.reg["X"][0] = value % 256

    @property
    def Y(self) -> bytes:
        return self.reg["Y"][0]

    @Y.setter
    def Y(self, value) -> None:
        self.reg["Y"][0] = value % 256
