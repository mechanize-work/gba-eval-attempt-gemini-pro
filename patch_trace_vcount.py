import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x06 => self.ppu.vcount as u8,', '0x06 => { println!("VCOUNT READ at cycle {}", self.wait_states); self.ppu.vcount as u8 },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
