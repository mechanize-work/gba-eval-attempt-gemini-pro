import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }""", """        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }""")

new_src = new_src.replace("""        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);""", """        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 1) as u32);""")

# For ARM branch
new_src = new_src.replace("""        if l_bit {
            self.regs[14] = self.regs[15].wrapping_sub(4);
        }

        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);""", """        if l_bit {
            self.regs[14] = self.regs[15].wrapping_sub(4);
        }

        self.regs[15] = self.regs[15].wrapping_add(4).wrapping_add((signed_offset << 2) as u32);""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
