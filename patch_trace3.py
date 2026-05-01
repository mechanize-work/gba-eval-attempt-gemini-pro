import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if cycle_count % 1000000 == 0 { println!("Trace: cycle {} PC={:08X}", cycle_count, pc); }',
                  'if _cycle_count < 200 { println!("Trace: PC={:08X} R0={:08X} R1={:08X} R2={:08X} R3={:08X} R4={:08X}", true_pc, gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[2], gba_mut().cpu.regs[3], gba_mut().cpu.regs[4]); }')
src = src.replace('let mut _cycle_count = 0;', 'let mut _cycle_count = 0;')
src = src.replace('let mut _count_a = 0;', '')
src = src.replace('_cycle_count += 1;', '_cycle_count += 1;')

with open("tests/compare.rs", "w") as f:
    f.write(src)
