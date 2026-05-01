import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("DMA0', 'println!("DMA0: {:08X} {:08X} {:04X} {:04X} DMA1: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[0].sad, gba_mut().mmu.dma[0].dad, gba_mut().mmu.dma[0].count, gba_mut().mmu.dma[0].ctrl, gba_mut().mmu.dma[1].sad, gba_mut().mmu.dma[1].dad, gba_mut().mmu.dma[1].count, gba_mut().mmu.dma[1].ctrl); }\n        // println!("DMA0')

with open("tests/compare.rs", "w") as f:
    f.write(src)
