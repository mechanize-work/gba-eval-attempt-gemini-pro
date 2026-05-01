import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        self.cycles += 1;', '        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        self.cycles += 2;')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
