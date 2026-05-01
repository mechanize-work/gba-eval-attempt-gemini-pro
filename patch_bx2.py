import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        if self.regs[15] == 0x08000D60 { println!("REACHED MAIN!"); }\n        if self.pipeline_empty {', '        if self.regs[15] == 0x08000196 && (self.cycles % 1000000 == 0) { println!("STUCK AT 08000196 LR={:08X} R0={:08X} R1={:08X}", self.regs[14], self.regs[0], self.regs[1]); }\n        if self.pipeline_empty {')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
