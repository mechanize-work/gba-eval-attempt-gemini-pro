import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let true_pc = pc.wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 });', 'let true_pc = pc.wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 });\n                if true_pc == 0x08000140 { println!("R1 BEFORE MEMSET 3 = {:08X}", gba_mut().cpu.regs[1]); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
