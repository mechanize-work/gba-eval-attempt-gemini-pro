import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count < 10 {', 'if gba_mut().cpu.regs[15] == 0x18 { println!("IRQ FIRED!"); }\n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
