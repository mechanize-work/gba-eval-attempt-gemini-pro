import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cpu.halted = false;\n                if self.cpu.saved_ime != 0xFFFF {', 'let was_halted = self.cpu.halted;\n                self.cpu.halted = false;\n                if self.cpu.saved_ime != 0xFFFF {')
src = src.replace('self.cpu.regs[14] = if self.cpu.halted { self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 }) } else if self.cpu.get_t() { self.cpu.regs[15].wrapping_add(2) } else if self.cpu.pipeline_empty {',
                  'self.cpu.regs[14] = if was_halted { self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 }) } else if self.cpu.pipeline_empty { self.cpu.regs[15].wrapping_add(4) } else if self.cpu.get_t() { self.cpu.regs[15].wrapping_add(2) } else { self.cpu.regs[15] };\n// ')
src = src.replace('self.cpu.regs[15].wrapping_add(4)\n                    } else {\n                        self.cpu.regs[15]\n                    };', '')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
