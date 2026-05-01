import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Map 0xE000:', 'println!("VRAM 0: {:02X} {:02X}", gba_mut().mmu.ppu.vram[0], gba_mut().mmu.ppu.vram[1]);\n        println!("Map 0xE000:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
