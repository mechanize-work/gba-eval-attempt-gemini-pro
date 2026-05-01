import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Thumb PC Load: use & !3 instead of & !2
src = src.replace("let addr = (self.regs[15] & !2).wrapping_add(imm);", "let addr = (self.regs[15] & !3).wrapping_add(imm);")
src = src.replace("self.regs[rd] = (self.regs[15] & !2).wrapping_add(imm);", "self.regs[rd] = (self.regs[15] & !3).wrapping_add(imm);")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)

with open("src/sys/gba.rs", "r") as f:
    gba = f.read()

gba = gba.replace("self.cycles += 4;", "self.cycles += 1;")

with open("src/sys/gba.rs", "w") as f:
    f.write(gba)
