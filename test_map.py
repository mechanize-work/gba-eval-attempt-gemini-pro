import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("BG2HOFS:', 'let map_val = (gba_mut().mmu.ppu.vram[0xE000] as u16) | ((gba_mut().mmu.ppu.vram[0xE001] as u16) << 8); println!("Map 0xE000: {:04X}", map_val);\n        println!("BG2HOFS:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
