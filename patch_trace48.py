import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if count_a % 100000 == 0 { println!("Frame {} PC={:08X} count_a={}", i, gba_mut().cpu.regs[15], count_a); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
