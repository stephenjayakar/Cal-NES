# CalNES Python
# ROM CLASS
# HANDLING READING OF .nes FILES


FILE_TYPE = b'NES'


class ROM:
    FILE = None
    header = None
    prg_rom_size = 0
    chr_rom_size = 0
    flags6 = 0
    flags7 = 0
    
    def __init__(self, filename: str):
        try:
            FILE = open(filename, "rb")
            self.FILE = FILE
            # The header is 16 bytes
            self.header = self.FILE.read(16)

            # First three bytes must say b'NES'
            if self.header[0:3] != FILE_TYPE:
                raise 
            
            # Number of 16384 byte program ROM pages
            self.prg_rom_size = self.header[4]

            # Number of 8192 byte character ROM pages
            self.chr_rom_size = self.header[5]

            # Bitfield 1
            self.flags6 = self.header[6]

            # Bitfield 2
            self.flags7 = self.header[7]

            # The prg rom data
            self.prg_rom = self.FILE.read(16 * 1024 * self.prg_rom_size)

            # TODO: Where's the chr rom data?  Is it after prg?
        
        except Exception as e:
            print("Invalid ROM")
            print(e)
            return None
        

# Main tests
if (__name__ == "__main__"):
    r = ROM("Super Mario Bros.nes")
