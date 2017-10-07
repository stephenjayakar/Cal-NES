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
    reg = {"A": 0,
           "X": 0,
           "Y": 0}

    opcode_to_instruction = {}

    def __init__(self, ram, PC_START = 0x8000):
        self.PC = PC_START
        self.ram = ram

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


    def get_mem(self, addr):
        return self.ram.mem_get(addr, 1)[0]

    def get_PC_byte(self):
        byte = self.get_mem(self.PC)
        self.PC += 1
        return byte

    def get_zero_page(self, offset=0):
        addr = self.get_PC_byte() + offset
        mem_byte = self.get_mem(addr)
        return mem_byte

    def get_zero_page_x(self):
        return self.get_zero_page(self.reg["x"])

    def get_zero_page_y(self):
        return self.get_zero_page(self.reg["y"])

    def get_absolute(self, offset=0):
        lower = self.get_PC_byte()
        upper = self.get_PC_byte()
        addr = (upper << 8 | lower) + offset
        mem_byte = self.get_mem(addr)
        return mem_byte

    def get_absolute_x(self):
        return self.get_absolute(self.reg["x"])

    def get_absolute_y(self):
        return self.get_absolute(self.reg["y"])

    def get_relative_addr(self):
        offset = self.convert_8bit_twos(self.get_PC_byte())
        addr = self.PC + offset
        return addr

    def get_indirect(self):
        """
        lower = self.get_PC_byte()
        upper = self.get_PC_byte()
        addr = (upper << 8 | lower)
        """
        return self.invalid_instruction(0)


    def run_instruction(self):
        opcode = self.get_PC_byte()
        self.evaluate_opcode(opcode)
        print(self.P)


    def evaluate_opcode(self, opcode):
        f = CPU.opcode_to_instruction[opcode]
        return f(opcode)


    def ADC(self, opcode):
        # ***** ADC(ADd with Carry) *****
        if opcode == 0x69: #Immediate, 2, 2
            return 0
        elif opcode == 0x65: #Zero Page, 2, 3
            return 0
        elif opcode == 0x75: #Zero Page,X, 2, 4
            return 0
        elif opcode == 0x6D: #Absolute, 3, 4
            return 0
        elif opcode == 0x7D: #Absolute,X, 3, 4
            return 0
        elif opcode == 0x79: #Absolute,Y, 3, 4
            return 0
        elif opcode == 0x61: #(Indirect,X) 2, 6
            return 0
        elif opcode == 0x71: #(Indirect,Y) 2, 5
            return 0


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
            return 0

        elif opcode == 0x31: #(Indirect,Y) 2, 5
            return 0
        else:
            return self.invalid_instruction(opcode)

        # update processor status
        self.set_Z(self.reg["A"])
        self.set_N(self.reg["A"])

    def ASL(self, opcode):
        #***** ASL - Arithmetic Shift Left: *****"""
        if opcode == 0x0A: #Accumulator, 1, 2
            return 0
        elif opcode == 0x06: #Zero Page, 2, 5
            return 0
        elif opcode == 0x16: #Zero Page,X, 2, 6
            return 0
        elif opcode == 0x0E: #Absolute, 3, 6
            return 0
        elif opcode == 0x1E: #Absolute,X, 3, 7
            return 0

    def BCC(self, opcode):
        #***** BCC - Branch if Carry Clear *****
        if opcode == 0x90:  #Relative, 2, 2
            return 0

    def BCS(self, opcode):
        #***** BCS - Branch if Carry Set *****
        if opcode == 0xB0:  #Relative, 2, 2
            return 0

    def BEQ(self, opcode):
        #***** BEQ - Branch if Equal *****
        if opcode == 0xF0:  #Relative, 2, 2
            return 0

    def BIT(self, opcode):
        #***** BIT - Bit Test *****
        if opcode == 0x24: #Zero Page, 2, 3
            return 0
        if opcode == 0x2C:  #Absolute, 3, 4
            return 0


    def BMI(self, opcode):
        #***** BMI - Branch if Minus *****
        if opcode == 0x30:  #Relative, 2, 2
            return 0

    def BNE(self, opcode):
        #***** BNE - Branch if Not Equal *****
        if opcode == 0xD0:  #Relative, 2, 2
            return 0

    def BPL(self, opcode):
        #***** BPL - Branch if Positive *****
        if opcode == 0x10:  #Relative, 2, 2
            return 0

    def BRK(self, opcode):
        #***** BRK - Force Interrupt *****
        if opcode == 0x00:  #Implied, 1, 7
            return 0

    def BVC(self, opcode):
        #***** BVC - Branch if OverFlow Clear *****
        if opcode == 0x50:  #Relative, 2, 2
            return 0

    def BVS(self, opcode):
        #***** BVS - Branch if OverFlow Set *****
        if opcode == 0x70:  #Relative, 2, 2
            return 0

    def CLC(self, opcode):
        #***** CLC - Clear Carry Flag *****
        if opcode == 0x18: #Implied, 1, 2
            return 0

    def CLD(self, opcode):
        #***** CLD - Clear Decimal Mode *****
        if opcode == 0xD8: #Implied, 1, 2
            return 0

    def CLI(self, opcode):
        #***** CLI - Clear Interrupt Disable *****
        if opcode == 0x58: #Implied, 1, 2
            return 0

    def CLV(self, opcode):
        #***** CLV - Clear Overflow Flag *****
        if opcode == 0xB8: #Implied, 1, 2
            return 0

    def CMP(self, opcode):
        #***** CMP - Compare *****
        if opcode == 0xC9: #Immediate 2, 2
            return 0
        elif opcode == 0xC5: #Zero Page 2, 3
            return 0
        elif opcode == 0xD5: #Zero Page,X 2, 4
            return 0
        elif opcode == 0xCD: #Absolute 3, 4
            return 0
        elif opcode == 0xDD: #Absolute,X 3, 4
            return 0
        elif opcode == 0xD9: #Absolute,Y, 3, 4
            return 0
        elif opcode == 0xC1: #(Indirect,X), 2, 6
            return 0
        elif opcode == 0xD1: #(Indirect),Y, 2, 5
            return 0

    def CPX(self, opcode):
        #***** CPX - Compare X Register *****
        if opcode == 0xE0: #Immediate 2, 2
            return 0
        elif opcode == 0xE4: #Zero Page 2, 3
            return 0
        elif opcode == 0xEC: #Absolute, 3, 4
            return 0

    def CPY(self, opcode):
        #***** CPY - Compare Y Register *****
        if opcode == 0xC0: #Immediate 2, 2
            return 0
        elif opcode == 0xC4: #Zero Page 2, 3
            return 0
        elif opcode == 0xCC: #Absolute, 3, 4
            return 0

    def DEC(self, opcode):
        #***** DEC - Decrement Memory *****
        if opcode == 0xC6: #Zero Page 2, 5
            return 0
        elif opcode == 0xD6: #Zero Page,X, 2, 6
            return 0
        elif opcode == 0xCE: #Absolute, 3, 6
            return 0
        elif opcode == 0xDE: #Absolute,X, 3, 7
            return 0

    def DEX(self, opcode):
        #***** DEX - Decrement X Register *****
        if opcode == 0xCA: #Implied 1, 2
            return 0

    def DEY(self, opcode):
        #***** DEY - Decrement Y Register *****
        if opcode == 0x88: #Implied 1, 2
            return 0

    def EOR(self, opcode):
        #***** EOR - Exclusive OR *****
        if opcode == 0x49:  # Immediate, 2, 2
            return 0
        elif opcode == 0x45:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x55:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0x4D:  # Absolute, 3, 4
            return 0
        elif opcode == 0x5D:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0x59:  # Absolute Y, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0x41:  # Indirect X, 2, 6
            return 0
        elif opcode == 0x51:  # Indirect Y, 2, 5 (+1 if page crossed)
            return 0

    def INC(self, opcode):
        #***** INC - Increment Memory *****
        if opcode == 0xE6:  # Zero Page, 2, 5
            return 0
        elif opcode == 0xF6:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0xEE:  # Absolute, 3, 6
            return 0
        elif opcode == 0xFE:  # Absolute X, 3, 7
            return 0

    def INX(self, opcode):
        #***** INX - Increment X Register *****
        if opcode == 0xE8:  # Implied, 1, 2
            return 0

    def INY(self, opcode):
        #***** INY - Increment Y Register *****
        if opcode == 0xC8:  # Implied, 1, 2
            return 0

    def JMP(self, opcode):
        #***** JMP - Jump *****
        if opcode == 0x4C:  # Absolute, 3, 3
            return 0
        elif opcode == 0x6C:  # Indirect, 3, 5
            return 0

    def JSR(self, opcode):
        #***** JSR - Jump to Subroutine *****
        if opcode == 0x20:  # Absolute, 3, 6
            return 0

    def LDA(self, opcode):
        #***** LDA - Load Accumulator *****
        if opcode == 0xA9:  # Immediate, 2, 2
            return 0
        elif opcode == 0xA5:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xB5:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xAD:  # Absolute, 3, 4
            return 0
        elif opcode == 0xBD:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0xB9:  # Absolute Y, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0xA1:  # Indirect X, 2, 6
            return 0
        elif opcode == 0xB1:  # Indirect Y, 2, 5 (+1 if page crossed)
            return 0

    def LDX(self, opcode):
        #***** LDX - Load X Register *****
        if opcode == 0xA2:  # Immediate, 2, 2
            return 0
        elif opcode == 0xA6:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xB6:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xAE:  # Absolute, 3, 4
            return 0
        elif opcode == 0xBE:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0

    def LDY(self, opcode):
        #***** LDY - Load Y Register *****
        if opcode == 0xA0:  # Immediate, 2, 2
            return 0
        elif opcode == 0xA4:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xB4:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xAC:  # Absolute, 3, 4
            return 0
        elif opcode == 0xBC:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0

    def LSR(self, opcode):
        # ***** LSR - Logical Shift Right *****
        if opcode == 0x4A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x46:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x56:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x4E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x5E:  # Absolute X, 3, 7
            return 0

    def NOP(self, opcode):
        # ***** NOP - No Operation *****
        if opcode == 0xEA:  # Implied, 1, 2
            return 0

    def ORA(self, opcode):
        #***** ORA - Logical Inclusive OR *****
        if opcode == 0x09:  # Immediate, 2, 2
            return 0
        elif opcode == 0x05:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x15:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0x0D:  # Absolute, 3, 4
            return 0
        elif opcode == 0x1D:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0x19:  # Absolute Y, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0x01:  # Indirect X, 2, 6
            return 0
        elif opcode == 0x11:  # Indirect Y, 2, 5 (+1 if page crossed)
            return 0

    def PHA(self, opcode):
        #***** PHA - Push Accumulator *****
        if opcode == 0x48:  # Implied, 1, 3
            return 0

    def PHP(self, opcode):
        #***** PHP - Push Processor Status *****
        if opcode == 0x08:  # Implied, 1, 3
            return 0

    def PLA(self, opcode):
        #***** PLA - Pull Accumulator *****
        if opcode == 0x68:  # Implied, 1, 4
            return 0

    def PLP(self, opcode):
        #***** PLP - Pull Processor Status *****
        if opcode == 0x28:  # Implied, 1, 4
            return 0

    def ROL(self, opcode):
        #***** ROL - Rotate Left *****
        if opcode == 0x2A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x26:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x36:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x2E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x3E:  # Absolute X, 3, 7
            return 0

    def ROR(self, opcode):
        #***** ROR - Rotate Right *****
        if opcode == 0x6A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x66:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x76:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x6E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x7E:  # Absolute X, 3, 7
            return 0

    def RTI(self, opcode):
        #***** RTI - Return from Interrupt *****
        if opcode == 0x40:  # Implied, 1, 6
            return 0

    def RTS(self, opcode):
        #***** RTS - Return from Subroutine *****
        if opcode == 0x60:  # Implied, 1, 6
            return 0

    def SBC(self, opcode):
        #***** SBC - Subtract with Carry *****
        if opcode == 0xE9:  # Immediate, 2, 2
            return 0
        elif opcode == 0xE5:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xF5:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xED:  # Absolute, 3, 4
            return 0
        elif opcode == 0xFD:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0xF9:  # Absolute Y, 3, 4 (+1 if page crossed)
            return 0
        elif opcode == 0xE1:  # Indirect X, 2, 6
            return 0
        elif opcode == 0xF1:  # Indirect Y, 2, 5 (+1 if page crossed)
            return 0

    def SEC(self, opcode):
        #***** SEC - Set Carry Flag *****
        if opcode == 0x38:  # Implied, 1, 2
            return 0

    def SED(self, opcode):
        #***** SED - Set Decimal Flag *****
        if opcode == 0xF8:  # Implied, 1, 2
            return 0

    def SEI(self, opcode):
        #***** SEI - Set Interrupt Disable *****
        if opcode == 0x78:  # Implied, 1, 2
            self.set_I(1)
            self.PC += 1
            return 0

    def STA(self, opcode):
        #***** STA - Store Accumulator *****
        if opcode == 0x85:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x95:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0x8D:  # Absolute, 3, 4
            return 0
        elif opcode == 0x9D:  # Absolute X, 3, 5
            return 0
        elif opcode == 0x99:  # Absolute Y, 3, 5
            return 0
        elif opcode == 0x81:  # Indirect X, 2, 6
            return 0
        elif opcode == 0x91:  # Indirect Y, 2, 6
            return 0

    def STX(self, opcode):
        #***** STX - Store X Register *****
        if opcode == 0x86:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x96:  # Zero Page Y, 2, 4
            return 0
        elif opcode == 0x8E:  # Absolute, 3, 4
            return 0

    def STY(self, opcode):
        #***** STY - Store Y Register *****
        if opcode == 0x84:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x94:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0x8C:  # Absolute, 3, 4
            return 0

    def TAX(self, opcode):
        #***** TAX - Transfer Accumulator to X *****
        if opcode == 0xAA:  # Implied, 1, 2
            return 0

    def TAY(self, opcode):
        #***** TAY - Transfer Accumulator to Y *****
        if opcode == 0xA8:  # Implied, 1, 2
            return 0

    def TSX(self, opcode):
        #***** TSX - Transfer Stack Pointer to X *****
        if opcode == 0xBA:  # Implied, 1, 2
            return 0

    def TXA(self, opcode):
        #***** TXA - Transfer X to Accumulator *****
        if opcode == 0x8A:  # Implied, 1, 2
            return 0

    def TXS(self, opcode):
        #***** TXS - Transfer X to Stack Pointer *****
        if opcode == 0x9A:  # Implied, 1, 2
            return 0

    def TYA(self, opcode):
        #***** TYA - Transfer Y to Accumulator *****
        if opcode == 0x98:  # Implied, 1, 2
            return 0


    def invalid_instruction(self, opcode):
        raise Exception


    def set_C(self, bit):
        self.set_bit_P(0, bit)

    def set_Z(self, reg):
        bit = not reg
        self.set_bit_P(1, bit)

    def set_I(self, bit):
        self.set_bit_P(2, bit)

    def set_D(self, bit):
        self.set_bit_P(3, bit)

    def set_B(self, bit):
        self.set_bit_P(4, bit)

    def set_V(self, bit):
        self.set_bit_P(5, bit)

    def set_N(self, reg):
        bit = reg >> 7
        self.set_bit_P(6, bit)


    def set_bit_P(self, pos, bit):
        mask = ~(1 << pos)
        self.P = self.P & mask | (bit << pos)


    def get_bit(self, target, pos):
        return (target >> pos) & 0b1


    def convert_8bit_twos(self, num):
        if (num & (1 << 7)):
            return -((num ^ 0xFF) + 1)
        else:
            return num


    # Prints contents of registers
    def _cpu_dump(self) -> str:
        return "Program Counter: " + str(self.PC) + "\n" + str(self.reg)
    
    def __str__(self) -> str:
        return self._cpu_dump()

    # TODO: Write this for the other registers
    #  Do we actually need this?  Why is a hashmap advantageous?
    @property
    def A(self) -> int:
        return self.reg["A"]

    @A.getter
    def A(self) -> int:
        return self.reg["A"]

    @A.setter
    def A(self, value) -> None:
        self.reg["A"] = value



if (__name__ == "__main__"):
    c = CPU()
    print(c)
    c.A = 2

