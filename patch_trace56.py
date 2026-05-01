import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x100 => (self.timers[0].counter >> 16) as u8,', '0x100 => { println!("TIMER 0 READ"); (self.timers[0].counter >> 16) as u8 },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
