import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("PAL0:', 'println!("Map value at 66: {:04X}", (gba_mut().mmu.ppu.vram[66] as u16) | ((gba_mut().mmu.ppu.vram[67] as u16) << 8));\n        println!("PAL0:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
