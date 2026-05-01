import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08', 'let pc = gba_mut().cpu.regs[15];\n                if _cycle_count > 204000 && _cycle_count < 205000 { println!("Trace: PC={:08X} R1={:08X} LR={:08X}", pc.wrapping_sub(2), gba_mut().cpu.regs[1], gba_mut().cpu.regs[14]); }\n                if pc == 0x08')

with open("tests/compare.rs", "w") as f:
    f.write(src)
