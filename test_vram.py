import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("PAL0:', 'let mut nonzero = 0; for i in 0..96*1024 { if gba_mut().mmu.ppu.vram[i] != 0 { nonzero += 1; } } println!("VRAM Non-zero bytes: {}", nonzero);\n        println!("PAL0:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
