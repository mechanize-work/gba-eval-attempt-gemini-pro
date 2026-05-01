import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('self.regs[14] = self.regs[15].wrapping_sub(2) | 1;',
                  'self.regs[14] = self.regs[15].wrapping_sub(2) | 1;\n            println!("BL SUFFIX: regs[15]={:08X} LR={:08X}", self.regs[15], self.regs[14]);')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
