import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('let is_32bit = (ctrl & 0x04000000) != 0;',
                  'let is_32bit = (ctrl & 0x04000000) != 0;\n                self.cycles += (count as usize) * (self.get_memory_cycles_32(src) + self.get_memory_cycles_32(dst));')

src = src.replace('0x0C => { // CpuFastSet\n                let src = self.regs[0] & !3;\n                let mut dst = self.regs[1] & !3;\n                let ctrl = self.regs[2];\n                let count = ctrl & 0x1FFFFF;\n                let fixed = (ctrl & 0x01000000) != 0;\n\n                let mut s = src;',
                  '0x0C => { // CpuFastSet\n                let src = self.regs[0] & !3;\n                let mut dst = self.regs[1] & !3;\n                let ctrl = self.regs[2];\n                let count = ctrl & 0x1FFFFF;\n                let fixed = (ctrl & 0x01000000) != 0;\n                self.cycles += (count as usize) * (self.get_memory_cycles_32(src) + self.get_memory_cycles_32(dst));\n\n                let mut s = src;')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
