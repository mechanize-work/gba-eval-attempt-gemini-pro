import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cpu.regs[14] = if self.cpu.halted { self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 }) } else if self.cpu.pipeline_empty {',
                  'self.cpu.regs[14] = if self.cpu.halted { self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 }) } else if self.cpu.get_t() { self.cpu.regs[15].wrapping_add(2) } else if self.cpu.pipeline_empty {')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
