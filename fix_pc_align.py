import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace("let addr = (self.regs[15] & !2).wrapping_add(imm);", "let addr = (self.regs[15] & !3).wrapping_add(imm);")
src = src.replace("self.regs[rd] = (self.regs[15] & !2).wrapping_add(imm);", "self.regs[rd] = (self.regs[15] & !3).wrapping_add(imm);")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
