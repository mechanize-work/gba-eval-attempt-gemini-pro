import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];', 'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000196 { println!("AT 08000196 LR={:08X} R0={:08X} R1={:08X} cycles={}", gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], _cycle_count); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
