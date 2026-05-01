import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("PAL0:', 'println!("BG2HOFS: {:04X}, BG2VOFS: {:04X}", gba_mut().mmu.ppu.bg2hofs, gba_mut().mmu.ppu.bg2vofs);\n        println!("PAL0:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
