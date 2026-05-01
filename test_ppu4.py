import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('for i in 0..512 { let c = (p[i*2] as u16)', 'let p = &gba_mut().mmu.ppu.palette;\n        for i in 0..512 { let c = (p[i*2] as u16)')

with open("tests/compare.rs", "w") as f:
    f.write(src)
