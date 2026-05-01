import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cpu.halted = false;', 'println!("CPU UNHALTED! IE={:04X} IF={:04X}", self.mmu.ie, self.mmu.i_f);\n                self.cpu.halted = false;')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
