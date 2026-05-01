import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if diff_count == 0 { println!("IO 50', 'if diff_count == 0 { println!("DMA0: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[0].sad, gba_mut().mmu.dma[0].dad, gba_mut().mmu.dma[0].count, gba_mut().mmu.dma[0].ctrl); }\n        if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
