import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if true_pc == 0x0800013E { println!("R0={:08X} R1={:08X} BEFORE SUBS", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]); }',
                  'if true_pc == 0x0800013E { println!("R0={:08X} R1={:08X} LR={:08X} BEFORE SUBS", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[14]); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
