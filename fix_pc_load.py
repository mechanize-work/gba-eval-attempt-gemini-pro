import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    fn execute_thumb_pc_load(&mut self, instr: u16, bus: &mut dyn Bus) {
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

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
