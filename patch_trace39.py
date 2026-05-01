import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if count_a % 100000 == 0 { println!("IE={:04X} IF={:04X}", gba_mut().mmu.ie, gba_mut().mmu.i_f); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
