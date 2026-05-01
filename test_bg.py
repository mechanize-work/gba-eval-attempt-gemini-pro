import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if count_a % 100000 == 0 { println!("BG2CNT={:04X} BG2HOFS={:04X}", gba_mut().mmu.ppu.bg2cnt, gba_mut().mmu.ppu.bg2hofs); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
