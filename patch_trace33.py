import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("DMA0', 'println!("DMA3: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[3].sad, gba_mut().mmu.dma[3].dad, gba_mut().mmu.dma[3].count, gba_mut().mmu.dma[3].ctrl); }\n        // println!("DMA0')

with open("tests/compare.rs", "w") as f:
    f.write(src)
