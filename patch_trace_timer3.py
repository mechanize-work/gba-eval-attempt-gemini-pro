import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('// IRQ\n                        if (control & 0x40) != 0 {\n                            self.mmu.i_f |= 1 << (3 + i);\n                        }', '// IRQ\n                        if (control & 0x40) != 0 {\n                            println!("TIMER {} IRQ at cycle {}!", i, self.cpu.cycles);\n                            self.mmu.i_f |= 1 << (3 + i);\n                        }')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
