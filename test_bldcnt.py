import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x0B0 => self.dma[0].sad =', '0x050 => { println!("BLDCNT: {:04X}", val); }\n                    0x051 => { println!("BLDCNT+1: {:04X}", val); }\n                    0x054 => { println!("BLDY: {:04X}", val); }\n                    0x0B0 => self.dma[0].sad =')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
