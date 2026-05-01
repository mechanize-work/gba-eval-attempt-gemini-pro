import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08', 'let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08000178 { println!("REACHED 08000178!"); }\n                if pc == 0x08')

with open("tests/compare.rs", "w") as f:
    f.write(src)
