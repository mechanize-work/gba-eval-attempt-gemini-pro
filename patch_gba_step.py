import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

new_step = """
            if (self.mmu.ie & self.mmu.i_f) != 0 {
                let was_halted = self.cpu.halted;
                self.cpu.halted = false;
                
                if self.cpu.saved_ime != 0xFFFF {
                    self.mmu.ime = self.cpu.saved_ime;
                    self.cpu.saved_ime = 0xFFFF;
                }

                if self.mmu.ime != 0 && (self.cpu.cpsr & 0x80) == 0 {
                    // Trigger IRQ exception
                    let old_cpsr = self.cpu.cpsr;
                    self.cpu.set_mode(crate::cpu::arm7tdmi::Mode::Irq);
                    self.cpu.spsr = old_cpsr;
                    
                    self.cpu.regs[14] = if was_halted {
                        self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 })
                    } else if self.cpu.pipeline_empty {
                        self.cpu.regs[15].wrapping_add(4)
                    } else if self.cpu.get_t() {
                        self.cpu.regs[15].wrapping_add(2)
                    } else {
                        self.cpu.regs[15]
                    };
                    
                    self.cpu.set_t(false);
                    self.cpu.set_i(true);
                    self.cpu.regs[15] = 0x00000018;
                    self.cpu.reload_pipeline();
                }
            }
"""

import re
src = re.sub(r'if \(self\.mmu\.ie & self\.mmu\.i_f\) != 0 \{\n.*self\.cpu\.reload_pipeline\(\);\n                \}\n            \}', new_step, src, flags=re.DOTALL)

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
