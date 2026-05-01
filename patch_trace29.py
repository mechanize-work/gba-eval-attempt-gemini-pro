import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Diff at {}:', 'if diff_count == 0 { println!("IO 50={:04X} 52={:04X} 54={:04X}", (gba_mut().mmu.ppu.bldcnt_0 as u16), gba_mut().mmu.ppu.bldalpha, gba_mut().mmu.ppu.bldy); } \n        println!("Diff at {}:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
