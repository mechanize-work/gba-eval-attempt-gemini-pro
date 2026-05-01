import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            // self.regs[15] is PC + 4 (instruction address + 4)
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }""", """    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }""")

new_src = new_src.replace("""    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);
        self.reload_pipeline();
    }""", """    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 1) as u32);
        self.reload_pipeline();
    }""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
