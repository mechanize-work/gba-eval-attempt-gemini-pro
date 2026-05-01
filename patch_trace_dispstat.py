import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x04000004 => self.ppu.dispstat as u8,', '0x04000004 => { println!("DISPSTAT READ"); self.ppu.dispstat as u8 },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
