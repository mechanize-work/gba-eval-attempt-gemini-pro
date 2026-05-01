import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("let base = if rn == 15 { self.regs[15] } else { self.regs[rn] };", "let base = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };")
new_src = new_src.replace("let base_val = if rn == 15 { self.regs[15] } else { self.regs[rn] };", "let base_val = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
