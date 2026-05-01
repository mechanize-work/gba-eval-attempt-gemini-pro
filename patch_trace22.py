import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if true_pc == 0x0800013E { println!("R0={:08X} R1={:08X} LR={:08X} BEFORE SUBS", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[14]); }',
                  'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000196 && gba_mut().cpu.regs[1] > 0x80000000 && _cycle_count % 10000 == 0 { println!("MEMSET BUG! LR={:08X} R0={:08X} R1={:08X}", gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
