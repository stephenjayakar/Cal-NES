from CalNES.NES import NES
import sys
import time

def main():
    filename = sys.argv[1]
    n = NES(filename)
    timer = time.time()
    while True:
        n.step()
        cur_time = time.time()
        if cur_time - timer >= 0.16639:
            timer = cur_time
            n.update_display()

main()
