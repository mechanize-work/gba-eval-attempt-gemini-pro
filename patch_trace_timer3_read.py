import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('0x10C => (self.timers[3].counter >> 16) as u8,', '0x10C => { println!("TIMER 3 READ"); (self.timers[3].counter >> 16) as u8 },')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
