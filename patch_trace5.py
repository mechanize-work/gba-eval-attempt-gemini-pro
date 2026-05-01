import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if _cycle_count < 100 { println!("Trace: PC={:08X}"', 'if true_pc == 0x08000198 { println!("MEMCPY CALLED from LR={:08X} R0={:08X} R1={:08X} R2={:08X} R4={:08X}", gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[2], gba_mut().cpu.regs[4]); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
