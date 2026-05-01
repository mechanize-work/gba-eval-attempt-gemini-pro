import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x0400000C => self.bg2cnt = (self.bg2cnt & 0xFF00) | (val as u16),', '0x0400000C => { self.bg2cnt = (self.bg2cnt & 0xFF00) | (val as u16); println!("BG2CNT WRITTEN!"); },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
