import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('                if self.cpu.saved_ime != 0xFFFF {\n                    self.mmu.ime = self.cpu.saved_ime;\n                    self.cpu.saved_ime = 0xFFFF;\n                }', '')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
