import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('        println!("DMA {} triggered! SAD={:08X} DAD={:08X} count={}", channel, self.dma[channel].sad, self.dma[channel].dad, self.dma[channel].count);\n        println!("DMA {} triggered! SAD={:08X} DAD={:08X} count={}", channel, self.dma[channel].sad, self.dma[channel].dad, self.dma[channel].count);', '        println!("DMA {} triggered! SAD={:08X} DAD={:08X} count={}", channel, self.dma[channel].sad, self.dma[channel].dad, self.dma[channel].count);')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
