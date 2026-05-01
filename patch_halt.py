import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('if self.mmu.ime != 0 && (self.mmu.ie & self.mmu.i_f) != 0 {', 'if (self.mmu.ie & self.mmu.i_f) != 0 {\n                self.cpu.halted = false;\n            }\n            if self.mmu.ime != 0 && (self.mmu.ie & self.mmu.i_f) != 0 {')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
