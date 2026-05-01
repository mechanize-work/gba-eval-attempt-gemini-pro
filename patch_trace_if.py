import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x202 => self.i_f &= !(val as u16),', '0x202 => { println!("IF CLEARED: {:04X}", val); self.i_f &= !(val as u16); },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
