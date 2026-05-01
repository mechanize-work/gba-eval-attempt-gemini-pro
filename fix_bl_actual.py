import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x0800) == 0 {
            let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
            self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
        } else {
            // self.regs[15] points to instruction + 4.
            // But we want the return address to be next instruction, which is instruction + 2.
            let next_pc = self.regs[15].wrapping_sub(2);
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc | 1;
            self.reload_pipeline();
        }
    }""", """    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x0800) == 0 {
            // First part of BL (H=0). offset is signed 11 bits.
            // Sign extend the 11-bit offset to 32 bits
            let mut signed_offset = offset;
            if (signed_offset & 0x400) != 0 {
                signed_offset |= !0x7FF;
            }
            self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
        } else {
            // Second part of BL (H=1)
            let next_pc = self.regs[15].wrapping_sub(2);
            // offset here is NOT sign extended, it's just shifted and added.
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc | 1;
            self.reload_pipeline();
        }
    }""")
print("Replaced" if new_src != src else "Unchanged")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
