import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace("let val = if i == 15 { self.regs[15].wrapping_add(2) } else { self.regs[i] };", "let val = if i == 15 { self.regs[15] } else { self.regs[i] };")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
