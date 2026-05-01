import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

import re
new_step = """    pub fn step(&mut self, bus: &mut dyn Bus) {
        if self.halted {
            self.cycles += 1;
            return;
        }

        if self.pipeline_empty {
            self.fill_pipeline(bus);
        }

        let instr = self.pipeline[0];
        self.pipeline[0] = self.pipeline[1];

        self.cycles += 2;

        if self.get_t() {"""

src = re.sub(r'    pub fn step\(&mut self, bus: &mut dyn Bus\) \{.*?if self\.get_t\(\) \{', new_step, src, flags=re.DOTALL, count=1)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
