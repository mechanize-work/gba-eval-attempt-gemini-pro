import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if gba_mut().cpu.regs[15] == 0x08012A46 && count_a % 10000 == 0 { println!("Stuck at 08012A46! R0={:08X} R1={:08X}", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
