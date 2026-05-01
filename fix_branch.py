import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Fix execute_thumb_cond_branch
src = src.replace("""    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }""", """    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            // regs[15] is currently PC + 2. Branch expects PC + 4.
            self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }""")

# Fix execute_thumb_uncond_branch
src = src.replace("""    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
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

# Fix execute_thumb_bl
src = src.replace("""    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x0800) == 0 {
            let mut signed_offset = offset;
            if (signed_offset & 0x400) != 0 {
                signed_offset |= !0x7FF;
            }
            self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
        } else {
            let next_pc = self.regs[15].wrapping_sub(2) | 1;
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc;
            self.reload_pipeline();
        }
    }""", """    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x0800) == 0 {
            let mut signed_offset = offset;
            if (signed_offset & 0x400) != 0 {
                signed_offset |= !0x7FF;
            }
            self.regs[14] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 12) as u32);
        } else {
            // Here, next_pc should be the instruction AFTER the suffix.
            // regs[15] is PC + 2. The instruction after the suffix is PC + 2.
            let next_pc = self.regs[15] | 1;
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc;
            self.reload_pipeline();
        }
    }""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
