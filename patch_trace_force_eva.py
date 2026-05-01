import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if i == 59 { gba_mut().mmu.ppu.bldalpha = (gba_mut().mmu.ppu.bldalpha & 0xFFE0) | 13; }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
