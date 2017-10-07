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
    
    def __init__(self, ram, PC_START = 0x8000):
        self.PC = PC_START
        self.ram = ram

    def run_instruction(self):
        opcode = self.get_byte()
        self.evaluate_opcode(opcode)
        print(self.P)

    def get_byte(self):
        return self.ram.mem_get(self.PC, 1)

    def evaluate_opcode(self, opcode: bytes):
        # ***** ADC(ADd with Carry) *****
        opcode = opcode[0]

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


        #***** AND - Logical AND *****
        elif opcode == 0x29: #Immediate, 2, 2
            #get imm
            self.PC += 1
            imm = self.get_byte()

            #operation AND
            self.reg["A"] &= imm

            #update processor status
            self.set_Z(self.reg["A"] == 0)
            self.set_N(self.get_bit(self.reg["A"], 7))

            self.PC += 1

        elif opcode == 0x25: #Zero Page, 2, 3
            return 0
        elif opcode == 0x35: #Zero Page,X, 2, 4
            return 0
        elif opcode == 0x2D: #Absolute, 3, 4
            return 0
        elif opcode == 0x3D: #Absolute,X, 3, 4
            return 0
        elif opcode == 0x39: #Absolute,Y, 3, 4
            return 0
        elif opcode == 0x21: #(Indirect,X) 2, 6
            return 0
        elif opcode == 0x31: #(Indirect,Y) 2, 5
            return 0


        #***** ASL - Arithmetic Shift Left: *****"""
        elif opcode == 0x0A: #Accumulator, 1, 2
            return 0
        elif opcode == 0x06: #Zero Page, 2, 5
            return 0
        elif opcode == 0x16: #Zero Page,X, 2, 6
            return 0
        elif opcode == 0x0E: #Absolute, 3, 6
            return 0
        elif opcode == 0x1E: #Absolute,X, 3, 7
            return 0


        #***** BCC - Branch if Carry Clear *****
        elif opcode == 0x90:  #Relative, 2, 2
            return 0


        #***** BCS - Branch if Carry Set *****
        elif opcode == 0xB0:  #Relative, 2, 2
            return 0


        #***** BEQ - Branch if Equal *****
        elif opcode == 0xF0:  #Relative, 2, 2
            return 0


        #***** BIT - Bit Test *****
        elif opcode == 0x24: #Zero Page, 2, 3
            return 0
        elif opcode == 0x2C:  #Absolute, 3, 4
            return 0


        #***** BMI - Branch if Minus *****
        elif opcode == 0x30:  #Relative, 2, 2
            return 0


        #***** BNE - Branch if Not Equal *****
        elif opcode == 0xD0:  #Relative, 2, 2
            return 0


        #***** BPL - Branch if Positive *****
        elif opcode == 0x10:  #Relative, 2, 2
            return 0


        #***** BRK - Force Interrupt *****
        elif opcode == 0x00:  #Implied, 1, 7
            return 0


        #***** BVC - Branch if OverFlow Clear *****
        elif opcode == 0x50:  #Relative, 2, 2
            return 0


        #***** BVS - Branch if OverFlow Set *****
        elif opcode == 0x70:  #Relative, 2, 2
            return 0


        #***** CLC - Clear Carry Flag *****
        elif opcode == 0x18: #Implied, 1, 2
            return 0


        #***** CLD - Clear Decimal Mode *****
        elif opcode == 0xD8: #Implied, 1, 2
            return 0


        #***** CLI - Clear Interrupt Disable *****
        elif opcode == 0x58: #Implied, 1, 2
            return 0

        #***** CLV - Clear Overflow Flag *****
        elif opcode == 0xB8: #Implied, 1, 2
            return 0


        #***** CMP - Compare *****
        elif opcode == 0xC9: #Immediate 2, 2
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


        #***** CPX - Compare X Register *****
        elif opcode == 0xE0: #Immediate 2, 2
            return 0
        elif opcode == 0xE4: #Zero Page 2, 3
            return 0
        elif opcode == 0xEC: #Absolute, 3, 4
            return 0


        #***** CPY - Compare Y Register *****
        elif opcode == 0xC0: #Immediate 2, 2
            return 0
        elif opcode == 0xC4: #Zero Page 2, 3
            return 0
        elif opcode == 0xCC: #Absolute, 3, 4
            return 0


        #***** DEC - Decrement Memory *****
        elif opcode == 0xC6: #Zero Page 2, 5
            return 0
        elif opcode == 0xD6: #Zero Page,X, 2, 6
            return 0
        elif opcode == 0xCE: #Absolute, 3, 6
            return 0
        elif opcode == 0xDE: #Absolute,X, 3, 7
            return 0


        #***** DEX - Decrement X Register *****
        elif opcode == 0xCA: #Implied 1, 2
            return 0


        #***** DEY - Decrement Y Register *****
        elif opcode == 0x88: #Implied 1, 2
            return 0


        #***** EOR - Exclusive OR *****
        elif opcode == 0x49:  # Immediate, 2, 2
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


        #***** INC - Increment Memory *****
        elif opcode == 0xE6:  # Zero Page, 2, 5
            return 0
        elif opcode == 0xF6:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0xEE:  # Absolute, 3, 6
            return 0
        elif opcode == 0xFE:  # Absolute X, 3, 7
            return 0


        #***** INX - Increment X Register *****
        elif opcode == 0xE8:  # Implied, 1, 2
            return 0


        #***** INY - Increment Y Register *****
        elif opcode == 0xC8:  # Implied, 1, 2
            return 0


        #***** JMP - Jump *****
        elif opcode == 0x4C:  # Absolute, 3, 3
            return 0
        elif opcode == 0x6C:  # Indirect, 3, 5
            return 0


        #***** JSR - Jump to Subroutine *****
        elif opcode == 0x20:  # Absolute, 3, 6
            return 0


        #***** LDA - Load Accumulator *****
        elif opcode == 0xA9:  # Immediate, 2, 2
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


        #***** LDX - Load X Register *****
        elif opcode == 0xA2:  # Immediate, 2, 2
            return 0
        elif opcode == 0xA6:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xB6:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xAE:  # Absolute, 3, 4
            return 0
        elif opcode == 0xBE:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0


        #***** LDY - Load Y Register *****
        elif opcode == 0xA0:  # Immediate, 2, 2
            return 0
        elif opcode == 0xA4:  # Zero Page, 2, 3
            return 0
        elif opcode == 0xB4:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0xAC:  # Absolute, 3, 4
            return 0
        elif opcode == 0xBC:  # Absolute X, 3, 4 (+1 if page crossed)
            return 0


        # ***** LSR - Logical Shift Right *****
        elif opcode == 0x4A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x46:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x56:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x4E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x5E:  # Absolute X, 3, 7
            return 0


        # ***** NOP - No Operation *****
        elif opcode == 0xEA:  # Implied, 1, 2
            return 0


        #***** ORA - Logical Inclusive OR *****
        elif opcode == 0x09:  # Immediate, 2, 2
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


        #***** PHA - Push Accumulator *****
        elif opcode == 0x48:  # Implied, 1, 3
            return 0


        #***** PHP - Push Processor Status *****
        elif opcode == 0x08:  # Implied, 1, 3
            return 0


        #***** PLA - Pull Accumulator *****
        elif opcode == 0x68:  # Implied, 1, 4
            return 0


        #***** PLP - Pull Processor Status *****
        elif opcode == 0x28:  # Implied, 1, 4
            return 0


        #***** ROL - Rotate Left *****
        elif opcode == 0x6A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x66:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x76:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x6E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x7E:  # Absolute X, 3, 7
            return 0


        #***** ROR - Rotate Right *****
        elif opcode == 0x6A:  # Accumulator, 1, 2
            return 0
        elif opcode == 0x66:  # Zero Page, 2, 5
            return 0
        elif opcode == 0x76:  # Zero Page X, 2, 6
            return 0
        elif opcode == 0x6E:  # Absolute, 3, 6
            return 0
        elif opcode == 0x7E:  # Absolute X, 3, 7
            return 0


        #***** RTI - Return from Interrupt *****
        elif opcode == 0x40:  # Implied, 1, 6
            return 0


        #***** RTS - Return from Subroutine *****
        elif opcode == 0x60:  # Implied, 1, 6
            return 0


        #***** SBC - Subtract with Carry *****
        elif opcode == 0xE9:  # Immediate, 2, 2
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


        #***** SEC - Set Carry Flag *****
        elif opcode == 0x38:  # Implied, 1, 2
            return 0


        #***** SED - Set Decimal Flag *****
        elif opcode == 0xF8:  # Implied, 1, 2
            return 0


        #***** SEI - Set Interrupt Disable *****
        elif opcode == 0x78:  # Implied, 1, 2
            self.set_I(1)
            self.PC += 1
            return 0


        #***** STA - Store Accumulator *****
        elif opcode == 0x85:  # Zero Page, 2, 3
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


        #***** STX - Store X Register *****
        elif opcode == 0x86:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x96:  # Zero Page Y, 2, 4
            return 0
        elif opcode == 0x8E:  # Absolute, 3, 4
            return 0


        #***** STY - Store Y Register *****
        elif opcode == 0x84:  # Zero Page, 2, 3
            return 0
        elif opcode == 0x94:  # Zero Page X, 2, 4
            return 0
        elif opcode == 0x8C:  # Absolute, 3, 4
            return 0


        #***** TAX - Transfer Accumulator to X *****
        elif opcode == 0xAA:  # Implied, 1, 2
            return 0


        #***** TAY - Transfer Accumulator to Y *****
        elif opcode == 0xA8:  # Implied, 1, 2
            return 0


        #***** TSX - Transfer Stack Pointer to X *****
        elif opcode == 0xBA:  # Implied, 1, 2
            return 0


        #***** TXA - Transfer X to Accumulator *****
        elif opcode == 0x8A:  # Implied, 1, 2
            return 0


        #***** TXS - Transfer X to Stack Pointer *****
        elif opcode == 0x9A:  # Implied, 1, 2
            return 0


        #***** TYA - Transfer Y to Accumulator *****
        elif opcode == 0x98:  # Implied, 1, 2
            return 0



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

    def get_bit(self, target, pos):
        return (target >> pos) & 0b1


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
