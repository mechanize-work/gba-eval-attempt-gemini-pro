import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08', 'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x0800016C { println!("MEMCPY ARGS R1={:08X} R2={:08X} R4={:08X}", gba_mut().cpu.regs[1], gba_mut().cpu.regs[2], gba_mut().cpu.regs[4]); }\n                if pc == 0x08')

with open("tests/compare.rs", "w") as f:
    f.write(src)
