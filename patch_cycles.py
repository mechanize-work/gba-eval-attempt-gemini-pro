import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

import re
new_step = """
    pub fn step(&mut self, bus: &mut dyn Bus) {
        if self.halted {
            self.cycles += 1;
            return;
        }

        if self.pipeline_empty {
            self.fill_pipeline(bus);
        }

        let instr = self.pipeline[0];
        self.pipeline[0] = self.pipeline[1];

        // Advanced cycle counting based on S/N cycles
        // For now, let's just make everything exactly 1 cycle per instruction.
        // wait, I tried that before and it gave EVA=0
        self.cycles += 1;

        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });

        if self.get_t() {"""

src = re.sub(r'    pub fn step\(&mut self, bus: &mut dyn Bus\) \{.*?if self\.get_t\(\) \{', new_step, src, flags=re.DOTALL)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
