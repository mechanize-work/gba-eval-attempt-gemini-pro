import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('let addr = (self.regs[15] & !2).wrapping_add(imm);',
                  'let addr = (self.regs[15] & !2).wrapping_add(imm);\n        if self.regs[15] > 0x08000138 && self.regs[15] < 0x08000148 { println!("PC_LOAD: regs[15]={:08X} imm={} addr={:08X} val={:08X}", self.regs[15], imm, addr, bus.read32(addr)); }')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
