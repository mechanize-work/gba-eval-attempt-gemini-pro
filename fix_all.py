import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Thumb conditional branch
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
            self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }""")

# Thumb uncond branch
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

# Thumb BL
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
            let next_pc = self.regs[15] | 1;
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc;
            self.reload_pipeline();
        }
    }""")

# Thumb PC Load
src = src.replace("""    fn execute_thumb_pc_load(&mut self, instr: u16, bus: &mut dyn Bus) {
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = ((instr & 0xFF) as u32) << 2;
        let addr = (self.regs[15] & !2).wrapping_add(imm);
        self.regs[rd] = bus.read32(addr);
    }""", """    fn execute_thumb_pc_load(&mut self, instr: u16, bus: &mut dyn Bus) {
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = ((instr & 0xFF) as u32) << 2;
        let addr = (self.regs[15].wrapping_add(2) & !2).wrapping_add(imm);
        self.regs[rd] = bus.read32(addr);
    }""")

# Thumb load address
src = src.replace("""            self.regs[rd] = (self.regs[15] & !2).wrapping_add(imm);""", """            self.regs[rd] = (self.regs[15].wrapping_add(2) & !2).wrapping_add(imm);""")

# ARM Branch
src = src.replace("""        if l_bit {
            self.regs[14] = self.regs[15].wrapping_sub(4);
        }

        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);""", """        if l_bit {
            self.regs[14] = self.regs[15];
        }

        self.regs[15] = self.regs[15].wrapping_add(4).wrapping_add((signed_offset << 2) as u32);""")

# ARM Load/Store
src = src.replace("""        let base = if rn == 15 { self.regs[15] } else { self.regs[rn] };""", """        let base = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };""")
src = src.replace("""        let base_val = if rn == 15 { self.regs[15] } else { self.regs[rn] };""", """        let base_val = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
