import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if count_a % 10000 == 0 { println!("PC={:08X} IME={}", gba_mut().cpu.regs[15], gba_mut().mmu.ime); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
