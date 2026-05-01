import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08', 'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000196 && gba_mut().cpu.regs[1] == 0 { println!("R1 IS 0! Z={}", gba_mut().cpu.get_z()); }\n                if pc == 0x08')

with open("tests/compare.rs", "w") as f:
    f.write(src)
