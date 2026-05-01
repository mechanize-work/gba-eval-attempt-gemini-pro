import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        if self.pipeline_empty {', '        if self.regs[15] == 0x08000D60 { println!("REACHED MAIN!"); }\n        if self.pipeline_empty {')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
