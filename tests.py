from CPU import CPU
from RAM import RAM

ram = RAM()
FILE = open("test_rom", 'rb')
ram.mem_set(0, bytearray(FILE.read()))

cpu = CPU(ram, 0)
cpu.run_all()
