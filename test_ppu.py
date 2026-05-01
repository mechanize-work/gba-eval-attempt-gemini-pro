import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let p = gba_mut().mmu.ppu.palette;', 'let p = &gba_mut().mmu.ppu.palette;')

with open("tests/compare.rs", "w") as f:
    f.write(src)
