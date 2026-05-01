import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if diff_count < 10 { println!("IO 50={:04X}', 'if diff_count < 10 { println!("Frame {} IO 50={:04X} 52={:04X} 54={:04X}", i, gba_mut().mmu.ppu.bldcnt, gba_mut().mmu.ppu.bldalpha, gba_mut().mmu.ppu.bldy); } \n        // if diff_count == 0 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
