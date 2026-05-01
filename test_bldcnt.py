import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x04000052 => self.bldalpha = (self.bldalpha & 0xFF00) | (val as u16),', '0x04000052 => { self.bldalpha = (self.bldalpha & 0xFF00) | (val as u16); println!("BLDALPHA 0x52={:02X}", val); },')
src = src.replace('0x04000053 => self.bldalpha = (self.bldalpha & 0x00FF) | ((val as u16) << 8),', '0x04000053 => { self.bldalpha = (self.bldalpha & 0x00FF) | ((val as u16) << 8); println!("BLDALPHA 0x53={:02X}", val); },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
