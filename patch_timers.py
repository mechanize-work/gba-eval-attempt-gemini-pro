import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

timer_struct = """
#[derive(Clone, Copy)]
pub struct Timer {
    pub reload: u16,
    pub control: u16,
    pub counter: u32,
}

impl Timer {
    pub fn new() -> Self {
        Self {
            reload: 0,
            control: 0,
            counter: 0,
        }
    }
}
"""

src = src.replace('#[derive(Clone, Copy)]\npub struct DmaChannel', timer_struct + '\n#[derive(Clone, Copy)]\npub struct DmaChannel')

src = src.replace('pub ppu: Ppu,\n    pub dma: [DmaChannel; 4],', 'pub ppu: Ppu,\n    pub dma: [DmaChannel; 4],\n    pub timers: [Timer; 4],')
src = src.replace('ppu: Ppu::new(),\n            dma: [DmaChannel::new(); 4],', 'ppu: Ppu::new(),\n            dma: [DmaChannel::new(); 4],\n            timers: [Timer::new(); 4],')

# Add reads
timer_read = """
                    0x100 => self.timers[0].counter as u8,
                    0x101 => (self.timers[0].counter >> 8) as u8,
                    0x102 => self.timers[0].control as u8,
                    0x103 => (self.timers[0].control >> 8) as u8,
                    0x104 => self.timers[1].counter as u8,
                    0x105 => (self.timers[1].counter >> 8) as u8,
                    0x106 => self.timers[1].control as u8,
                    0x107 => (self.timers[1].control >> 8) as u8,
                    0x108 => self.timers[2].counter as u8,
                    0x109 => (self.timers[2].counter >> 8) as u8,
                    0x10A => self.timers[2].control as u8,
                    0x10B => (self.timers[2].control >> 8) as u8,
                    0x10C => self.timers[3].counter as u8,
                    0x10D => (self.timers[3].counter >> 8) as u8,
                    0x10E => self.timers[3].control as u8,
                    0x10F => (self.timers[3].control >> 8) as u8,
"""
src = src.replace('0x200 => self.ie as u8,', timer_read + '0x200 => self.ie as u8,')

# Add writes
timer_write = """
                    0x100 => { self.timers[0].reload = (self.timers[0].reload & 0xFF00) | (val as u16); self.timers[0].counter = self.timers[0].reload as u32; },
                    0x101 => { self.timers[0].reload = (self.timers[0].reload & 0x00FF) | ((val as u16) << 8); self.timers[0].counter = self.timers[0].reload as u32; },
                    0x102 => self.timers[0].control = (self.timers[0].control & 0xFF00) | (val as u16),
                    0x103 => self.timers[0].control = (self.timers[0].control & 0x00FF) | ((val as u16) << 8),
                    0x104 => { self.timers[1].reload = (self.timers[1].reload & 0xFF00) | (val as u16); self.timers[1].counter = self.timers[1].reload as u32; },
                    0x105 => { self.timers[1].reload = (self.timers[1].reload & 0x00FF) | ((val as u16) << 8); self.timers[1].counter = self.timers[1].reload as u32; },
                    0x106 => self.timers[1].control = (self.timers[1].control & 0xFF00) | (val as u16),
                    0x107 => self.timers[1].control = (self.timers[1].control & 0x00FF) | ((val as u16) << 8),
                    0x108 => { self.timers[2].reload = (self.timers[2].reload & 0xFF00) | (val as u16); self.timers[2].counter = self.timers[2].reload as u32; },
                    0x109 => { self.timers[2].reload = (self.timers[2].reload & 0x00FF) | ((val as u16) << 8); self.timers[2].counter = self.timers[2].reload as u32; },
                    0x10A => self.timers[2].control = (self.timers[2].control & 0xFF00) | (val as u16),
                    0x10B => self.timers[2].control = (self.timers[2].control & 0x00FF) | ((val as u16) << 8),
                    0x10C => { self.timers[3].reload = (self.timers[3].reload & 0xFF00) | (val as u16); self.timers[3].counter = self.timers[3].reload as u32; },
                    0x10D => { self.timers[3].reload = (self.timers[3].reload & 0x00FF) | ((val as u16) << 8); self.timers[3].counter = self.timers[3].reload as u32; },
                    0x10E => self.timers[3].control = (self.timers[3].control & 0xFF00) | (val as u16),
                    0x10F => self.timers[3].control = (self.timers[3].control & 0x00FF) | ((val as u16) << 8),
"""
src = src.replace('0x200 => self.ie = (self.ie & 0xFF00) | (val as u16),', timer_write + '0x200 => self.ie = (self.ie & 0xFF00) | (val as u16),')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
