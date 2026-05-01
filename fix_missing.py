import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

missing_funcs = """
    fn execute_thumb_bx(&mut self, instr: u16, bus: &mut dyn Bus) {
        let rm = (instr >> 3) & 0xF;
        let val = self.regs[rm as usize];
        self.set_t((val & 1) != 0);
        self.regs[15] = val & !1;
        self.reload_pipeline();
    }
    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }
    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);
        self.reload_pipeline();
    }
    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x1000) == 0 {
            let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
            self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
        } else {
            let next_pc = self.regs[15].wrapping_sub(2);
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
            self.regs[14] = next_pc | 1;
            self.reload_pipeline();
        }
    }
"""

end_pos = src.rfind("fn execute_arm_data_processing")
new_src = src[:end_pos] + missing_funcs + "\n    " + src[end_pos:]

# Remove the incorrect append I did
new_src = new_src.replace("\nimpl Cpu {\n    // missing functions\n}\n", "")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
