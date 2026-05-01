import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

# Fix read
src = src.replace('0x100 => self.timers[0].counter as u8,', '0x100 => (self.timers[0].counter >> 16) as u8,')
src = src.replace('0x101 => (self.timers[0].counter >> 8) as u8,', '0x101 => (self.timers[0].counter >> 24) as u8,')
src = src.replace('0x104 => self.timers[1].counter as u8,', '0x104 => (self.timers[1].counter >> 16) as u8,')
src = src.replace('0x105 => (self.timers[1].counter >> 8) as u8,', '0x105 => (self.timers[1].counter >> 24) as u8,')
src = src.replace('0x108 => self.timers[2].counter as u8,', '0x108 => (self.timers[2].counter >> 16) as u8,')
src = src.replace('0x109 => (self.timers[2].counter >> 8) as u8,', '0x109 => (self.timers[2].counter >> 24) as u8,')
src = src.replace('0x10C => self.timers[3].counter as u8,', '0x10C => (self.timers[3].counter >> 16) as u8,')
src = src.replace('0x10D => (self.timers[3].counter >> 8) as u8,', '0x10D => (self.timers[3].counter >> 24) as u8,')

# Fix write
src = src.replace('0x100 => { self.timers[0].reload = (self.timers[0].reload & 0xFF00) | (val as u16); self.timers[0].counter = self.timers[0].reload as u32; },', '0x100 => { self.timers[0].reload = (self.timers[0].reload & 0xFF00) | (val as u16); },')
src = src.replace('0x101 => { self.timers[0].reload = (self.timers[0].reload & 0x00FF) | ((val as u16) << 8); self.timers[0].counter = self.timers[0].reload as u32; },', '0x101 => { self.timers[0].reload = (self.timers[0].reload & 0x00FF) | ((val as u16) << 8); },')

src = src.replace('0x104 => { self.timers[1].reload = (self.timers[1].reload & 0xFF00) | (val as u16); self.timers[1].counter = self.timers[1].reload as u32; },', '0x104 => { self.timers[1].reload = (self.timers[1].reload & 0xFF00) | (val as u16); },')
src = src.replace('0x105 => { self.timers[1].reload = (self.timers[1].reload & 0x00FF) | ((val as u16) << 8); self.timers[1].counter = self.timers[1].reload as u32; },', '0x105 => { self.timers[1].reload = (self.timers[1].reload & 0x00FF) | ((val as u16) << 8); },')

src = src.replace('0x108 => { self.timers[2].reload = (self.timers[2].reload & 0xFF00) | (val as u16); self.timers[2].counter = self.timers[2].reload as u32; },', '0x108 => { self.timers[2].reload = (self.timers[2].reload & 0xFF00) | (val as u16); },')
src = src.replace('0x109 => { self.timers[2].reload = (self.timers[2].reload & 0x00FF) | ((val as u16) << 8); self.timers[2].counter = self.timers[2].reload as u32; },', '0x109 => { self.timers[2].reload = (self.timers[2].reload & 0x00FF) | ((val as u16) << 8); },')

src = src.replace('0x10C => { self.timers[3].reload = (self.timers[3].reload & 0xFF00) | (val as u16); self.timers[3].counter = self.timers[3].reload as u32; },', '0x10C => { self.timers[3].reload = (self.timers[3].reload & 0xFF00) | (val as u16); },')
src = src.replace('0x10D => { self.timers[3].reload = (self.timers[3].reload & 0x00FF) | ((val as u16) << 8); self.timers[3].counter = self.timers[3].reload as u32; },', '0x10D => { self.timers[3].reload = (self.timers[3].reload & 0x00FF) | ((val as u16) << 8); },')

src = src.replace('0x102 => self.timers[0].control = (self.timers[0].control & 0xFF00) | (val as u16),', '0x102 => { let old = self.timers[0].control; self.timers[0].control = (old & 0xFF00) | (val as u16); if (old & 0x80) == 0 && (self.timers[0].control & 0x80) != 0 { self.timers[0].counter = (self.timers[0].reload as u32) << 16; } },')
src = src.replace('0x106 => self.timers[1].control = (self.timers[1].control & 0xFF00) | (val as u16),', '0x106 => { let old = self.timers[1].control; self.timers[1].control = (old & 0xFF00) | (val as u16); if (old & 0x80) == 0 && (self.timers[1].control & 0x80) != 0 { self.timers[1].counter = (self.timers[1].reload as u32) << 16; } },')
src = src.replace('0x10A => self.timers[2].control = (self.timers[2].control & 0xFF00) | (val as u16),', '0x10A => { let old = self.timers[2].control; self.timers[2].control = (old & 0xFF00) | (val as u16); if (old & 0x80) == 0 && (self.timers[2].control & 0x80) != 0 { self.timers[2].counter = (self.timers[2].reload as u32) << 16; } },')
src = src.replace('0x10E => self.timers[3].control = (self.timers[3].control & 0xFF00) | (val as u16),', '0x10E => { let old = self.timers[3].control; self.timers[3].control = (old & 0xFF00) | (val as u16); if (old & 0x80) == 0 && (self.timers[3].control & 0x80) != 0 { self.timers[3].counter = (self.timers[3].reload as u32) << 16; } },')


with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
