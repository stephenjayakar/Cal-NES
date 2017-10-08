from CPU import CPU
from RAM import RAM

r = RAM()
FILE = open("test_rom", 'rb')
r.mem_set(0, bytearray(FILE.read()))

c = CPU(r, 0)
c.run_instruction()
