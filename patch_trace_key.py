import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x04000130 => self.ppu.keyinput as u8,', '0x04000130 => { println!("KEYINPUT READ"); self.ppu.keyinput as u8 },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
