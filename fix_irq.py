import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace("self.cpu.regs[14] = self.cpu.regs[15]; // Not wrapping_add 4 since we are currently executing", "self.cpu.regs[14] = if self.cpu.get_t() { self.cpu.regs[15] } else { self.cpu.regs[15].wrapping_sub(4) };")

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
