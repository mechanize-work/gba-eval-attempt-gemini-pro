import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    pub fn step(&mut self, bus: &mut dyn Bus) {
        if self.pipeline_empty {
            self.fill_pipeline(bus);
        }

        let instr = self.pipeline[0];
        self.pipeline[0] = self.pipeline[1];

        if self.get_t() {
            self.execute_thumb(instr as u16, bus);
            if !self.pipeline_empty {
                self.pipeline[1] = bus.read16(self.regs[15]) as u32;
                self.regs[15] = self.regs[15].wrapping_add(2);
            }
        } else {
            if self.check_cond(instr >> 28) {
                self.execute_arm(instr, bus);
            }
            if !self.pipeline_empty {
                self.pipeline[1] = bus.read32(self.regs[15]);
                self.regs[15] = self.regs[15].wrapping_add(4);
            }
        }
    }""", """    pub fn step(&mut self, bus: &mut dyn Bus) {
        if self.pipeline_empty {
            self.fill_pipeline(bus);
        }

        let instr = self.pipeline[0];
        self.pipeline[0] = self.pipeline[1];

        if self.get_t() {
            // Note: PC is 4 bytes ahead during execution!
            // Wait, we add 2 to PC *before* execution so that PC read by instruction is PC+4
            self.pipeline[1] = bus.read16(self.regs[15]) as u32;
            self.regs[15] = self.regs[15].wrapping_add(2);
            self.execute_thumb(instr as u16, bus);
        } else {
            self.pipeline[1] = bus.read32(self.regs[15]);
            self.regs[15] = self.regs[15].wrapping_add(4);
            if self.check_cond(instr >> 28) {
                self.execute_arm(instr, bus);
            }
        }
    }""")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
