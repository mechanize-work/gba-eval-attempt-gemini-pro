import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x208 => self.ime = (self.ime & 0xFF00) | (val as u16),', '0x208 => { println!("IME WRITTEN: {:02X}", val); self.ime = (self.ime & 0xFF00) | (val as u16); },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
