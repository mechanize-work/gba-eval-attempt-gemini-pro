import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("End of frame {}: PC={:08X}", i, gba_mut().cpu.regs[15]);', 'println!("End of frame {}: PC={:08X} R0={:08X} R1={:08X}", i, gba_mut().cpu.regs[15], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]);')
src = src.replace('if true_pc == 0x08000198 { println!("MEMCPY', '//')

with open("tests/compare.rs", "w") as f:
    f.write(src)
