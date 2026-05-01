import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Fix ARM branch
src = src.replace("""        self.regs[15] = self.regs[15].wrapping_add(4).wrapping_add((signed_offset << 2) as u32);""", """        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);""")

# Fix ARM LDR/STR
src = src.replace("""let base = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };""", """let base = if rn == 15 { self.regs[15] } else { self.regs[rn] };""")
src = src.replace("""let base_val = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };""", """let base_val = if rn == 15 { self.regs[15] } else { self.regs[rn] };""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
