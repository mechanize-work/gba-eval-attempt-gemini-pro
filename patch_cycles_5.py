import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        self.cycles += 2;', '        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        self.cycles += 1;')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cycles >= 600', 'self.cycles >= 3000')
src = src.replace('self.cycles -= 600', 'self.cycles -= 3000')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
