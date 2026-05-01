import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Map 0xE000:', 'println!("BG0CNT: {:04X}, BG1CNT: {:04X}, BG2CNT: {:04X}, BG3CNT: {:04X}", gba_mut().mmu.ppu.bg0cnt, gba_mut().mmu.ppu.bg1cnt, gba_mut().mmu.ppu.bg2cnt, gba_mut().mmu.ppu.bg3cnt);\n        println!("Map 0xE000:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
