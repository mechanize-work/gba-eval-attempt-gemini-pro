import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Map 0xE042:', 'println!("VRAM 120: {:02X}", gba_mut().mmu.ppu.vram[120]);\n        println!("Map 0xE042:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
