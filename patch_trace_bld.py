import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x04000052 => self.bldalpha = (self.bldalpha & 0xFF00) | (val as u16),', '0x04000052 => { println!("EVA WRITTEN: {:02X}", val); self.bldalpha = (self.bldalpha & 0xFF00) | (val as u16); },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
