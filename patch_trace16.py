import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if _cycle_count > 204000', 'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000140 { println!("R1 BEFORE MEMSET 3 = {:08X}", gba_mut().cpu.regs[1]); }\n                if _cycle_count > 204000')

with open("tests/compare.rs", "w") as f:
    f.write(src)
