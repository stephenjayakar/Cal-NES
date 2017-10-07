class CPU:
    # Program Counter
    PC = 0
    # Processor Status
    P = 0
    # Stack Pointer
    SP = 0
    
    # Registers
    reg = {"A": 0,
           "X": 0,
           "Y": 0}
    
    def __init__(self, PC_START = 0x600):
        self.PC = PC_START

    def run_instruction(self, b: bytes) -> bool:
        return False

    # Load immediate -> register
    def _ld_immediate(self, register: str, immediate: int):
        self.reg[register] = immediate

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
