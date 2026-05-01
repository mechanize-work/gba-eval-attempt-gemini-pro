import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count < 10 {', 'if diff_count == 0 { println!("IE={:04X} IF={:04X} DISPSTAT={:04X}", gba_mut().mmu.ie, gba_mut().mmu.i_f, gba_mut().mmu.ppu.dispstat); }\n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
