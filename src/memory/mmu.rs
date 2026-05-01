use super::bus::Bus;
use crate::ppu::Ppu;

pub struct Mmu {
    pub bios: Vec<u8>,
    pub ewram: Box<[u8; 256 * 1024]>,
    pub iwram: Box<[u8; 32 * 1024]>,
    pub rom: Vec<u8>,
    pub sram: Box<[u8; 64 * 1024]>,
    pub ppu: Ppu,
    pub wait_states: usize,
    pub ie: u16,
    pub i_f: u16,
    pub ime: u16,
}

impl Mmu {
    pub fn new() -> Self {
        Self {
            bios: vec![0; 16 * 1024],
            ewram: Box::new([0; 256 * 1024]),
            iwram: Box::new([0; 32 * 1024]),
            rom: vec![0; 32 * 1024 * 1024],
            sram: Box::new([0; 64 * 1024]),
            ppu: Ppu::new(),
            wait_states: 0,
            ie: 0,
            i_f: 0,
            ime: 0,
        }
    }
}

impl Bus for Mmu {
    fn read8(&mut self, addr: u32) -> u8 {
        match addr >> 24 {
            0x00 => if addr < 0x4000 { self.bios[addr as usize] } else { 0 },
            0x02 => self.ewram[(addr & 0x3FFFF) as usize],
            0x03 => self.iwram[(addr & 0x7FFF) as usize],
            0x04 => {
                match addr & 0xFFFFFF {
                    0x200 => self.ie as u8,
                    0x201 => (self.ie >> 8) as u8,
                    0x202 => self.i_f as u8,
                    0x203 => (self.i_f >> 8) as u8,
                    0x208 => self.ime as u8,
                    0x209 => (self.ime >> 8) as u8,
                    _ => self.ppu.read8(addr),
                }
            },
            0x05 => self.ppu.palette[(addr & 0x3FF) as usize],
            0x06 => {
                let offset = addr & 0x1FFFF;
                if offset < 96 * 1024 {
                    self.ppu.vram[offset as usize]
                } else {
                    0
                }
            }
            0x07 => self.ppu.oam[(addr & 0x3FF) as usize],
            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => {
                let offset = addr & 0x1FFFFFF;
                if offset < self.rom.len() as u32 {
                    self.rom[offset as usize]
                } else {
                    0
                }
            }
            0x0E => self.sram[(addr & 0xFFFF) as usize],
            _ => 0,
        }
    }

    fn read16(&mut self, addr: u32) -> u16 {
        let addr = addr & !1;
        (self.read8(addr) as u16) | ((self.read8(addr + 1) as u16) << 8)
    }

    fn read32(&mut self, addr: u32) -> u32 {
        let addr = addr & !3;
        (self.read8(addr) as u32) | ((self.read8(addr + 1) as u32) << 8) | ((self.read8(addr + 2) as u32) << 16) | ((self.read8(addr + 3) as u32) << 24)
    }

    fn write8(&mut self, addr: u32, val: u8) {
        match addr >> 24 {
            0x02 => self.ewram[(addr & 0x3FFFF) as usize] = val,
            0x03 => self.iwram[(addr & 0x7FFF) as usize] = val,
            0x04 => {
                match addr & 0xFFFFFF {
                    0x200 => self.ie = (self.ie & 0xFF00) | (val as u16),
                    0x201 => self.ie = (self.ie & 0x00FF) | ((val as u16) << 8),
                    0x202 => self.i_f &= !(val as u16),
                    0x203 => self.i_f &= !((val as u16) << 8),
                    0x208 => self.ime = (self.ime & 0xFF00) | (val as u16),
                    0x209 => self.ime = (self.ime & 0x00FF) | ((val as u16) << 8),
                    _ => self.ppu.write8(addr, val),
                }
            },
            0x05 => self.ppu.palette[(addr & 0x3FF) as usize] = val,
            0x06 => {
                let offset = addr & 0x1FFFF;
                if offset < 96 * 1024 {
                    self.ppu.vram[offset as usize] = val;
                }
            }
            0x07 => self.ppu.oam[(addr & 0x3FF) as usize] = val,
            0x0E => self.sram[(addr & 0xFFFF) as usize] = val,
            _ => {}
        }
    }

    fn write16(&mut self, addr: u32, val: u16) {
        let addr = addr & !1;
        self.write8(addr, val as u8);
        self.write8(addr + 1, (val >> 8) as u8);
    }

    fn write32(&mut self, addr: u32, val: u32) {
        let addr = addr & !3;
        self.write8(addr, val as u8);
        self.write8(addr + 1, (val >> 8) as u8);
        self.write8(addr + 2, (val >> 16) as u8);
        self.write8(addr + 3, (val >> 24) as u8);
    }
}
