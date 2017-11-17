class RAM:
    memory = None
    
    def __init__(self):
        self.memory = bytearray(0x10000)

    def mem_set(self, offset: int, data: bytearray) -> None:
        length = len(data)
        self.memory[offset:offset + length] = data

    # Read from start to length in bytes
    def mem_get(self, offset: int, length: int) -> bytes:
        # max_index = offset + length
        # if max_index < len(self.memory):
        return bytes(self.memory[offset:offset + length])        
