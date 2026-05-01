import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('BG0CNT: {:04X}", gba_mut().mmu.ppu.dispcnt, gba_mut().mmu.ppu.bg0cnt)', 'BG2CNT: {:04X}", gba_mut().mmu.ppu.dispcnt, gba_mut().mmu.ppu.bg2cnt)')

with open("tests/compare.rs", "w") as f:
    f.write(src)
