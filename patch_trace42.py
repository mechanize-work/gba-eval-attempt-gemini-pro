import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if count_a % 100000 == 0 { println!("Frame {} EVA={}", i, gba_mut().mmu.ppu.bldalpha & 0x1F); }', 'println!("Frame {} EVA={}", i, gba_mut().mmu.ppu.bldalpha & 0x1F);')

with open("tests/compare.rs", "w") as f:
    f.write(src)
