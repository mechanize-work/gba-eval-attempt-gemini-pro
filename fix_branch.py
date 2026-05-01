import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Replace execute_thumb_cond_branch
start = src.find("    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {")
end = src.find("    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {")

new_func = """    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            // self.regs[15] is PC + 4 (instruction address + 4)
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }
"""

src = src[:start] + new_func + src[end:]

start = src.find("    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {")
end = src.find("    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {")

new_func = """    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);
        self.reload_pipeline();
    }
"""

src = src[:start] + new_func + src[end:]

start = src.find("    fn execute_arm_branch(&mut self, instr: u32, bus: &mut dyn Bus) {")
end = src.find("    fn execute_arm_swi(&mut self, instr: u32, bus: &mut dyn Bus) {")

new_func = """    fn execute_arm_branch(&mut self, instr: u32, bus: &mut dyn Bus) {
        let l_bit = (instr >> 24) & 1 != 0;
        let offset = instr & 0x00FFFFFF;
        let signed_offset = if (offset & 0x00800000) != 0 {
            offset | 0xFF000000
        } else {
            offset
        };

        if l_bit {
            self.regs[14] = self.regs[15].wrapping_sub(4);
        }

        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);
        self.reload_pipeline();
    }

"""

src = src[:start] + new_func + src[end:]

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
