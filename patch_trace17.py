import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000140 { println!("R1 BEFORE MEMSET 3 = {:08X}", gba_mut().cpu.regs[1]); }',
                  'let pc = gba_mut().cpu.regs[15];\n                let true_pc = pc.wrapping_sub(4);\n                if true_pc == 0x08000140 { println!("R1 BEFORE MEMSET 3 = {:08X}", gba_mut().cpu.regs[1]); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
