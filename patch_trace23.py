import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Frame 1 differences:',
                  'println!("PAL0: {:02X}{:02X}, DISPCNT: {:04X}, BG0CNT: {:04X}", gba_mut().mmu.ppu.palette[1], gba_mut().mmu.ppu.palette[0], gba_mut().mmu.ppu.dispcnt, gba_mut().mmu.ppu.bg0cnt);\n        println!("Frame 1 differences:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
