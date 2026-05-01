import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

start = src.find("fn execute_thumb_bl")
end = src.find("}", src.find("self.reload_pipeline();", start)) + 1

bl_correct = """    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
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
            println!("BL Target: {:08X}", self.regs[15]);
            self.reload_pipeline();
        }
    }"""

new_src = src[:start] + bl_correct + src[end:]

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
