import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('    fn execute_thumb_bx(&mut self, instr: u16, bus: &mut dyn Bus) {\n        let rm = ((instr >> 3) & 0xF) as usize;\n        let target = self.regs[rm];',
                  '    fn execute_thumb_bx(&mut self, instr: u16, bus: &mut dyn Bus) {\n        let rm = ((instr >> 3) & 0xF) as usize;\n        let target = self.regs[rm];\n        if target == 0 { println!("BX 0! SP={:08X} LR={:08X} PC={:08X}", self.regs[13], self.regs[14], self.regs[15]); }')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
