import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""        // Writeback happens only if NOT loading into the base register!
        if !l_bit || (r_list & (1 << rb)) == 0 {
            self.regs[rb] = addr;
        }""", """        // Writeback happens only if NOT loading into the base register!
        if !l_bit || (r_list & (1 << rb)) == 0 {
            self.regs[rb] = addr;
        }""")
