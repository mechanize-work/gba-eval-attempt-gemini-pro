import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Map 0xE000: {:04X}", map_val);', 'let map_val2 = (gba_mut().mmu.ppu.vram[0xE042] as u16) | ((gba_mut().mmu.ppu.vram[0xE043] as u16) << 8); println!("Map 0xE042: {:04X}", map_val2);')

with open("tests/compare.rs", "w") as f:
    f.write(src)
