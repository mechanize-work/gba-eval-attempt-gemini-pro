use super::bus::Bus;
use crate::ppu::Ppu;


#[derive(Clone, Copy)]
pub struct DmaChannel {
    pub sad: u32,
    pub dad: u32,
    pub count: u16,
    pub ctrl: u16,
}

impl DmaChannel {

    pub fn new() -> Self {
        Self {
            sad: 0,
            dad: 0,
            count: 0,
            ctrl: 0,
        }
    }
}



pub struct Mmu {
    pub bios: Vec<u8>,
    pub ewram: Box<[u8; 256 * 1024]>,
    pub iwram: Box<[u8; 32 * 1024]>,
    pub rom: Vec<u8>,
    pub sram: Box<[u8; 64 * 1024]>,
    pub ppu: Ppu,
    pub dma: [DmaChannel; 4],
    pub wait_states: usize,
    pub ie: u16,
    pub i_f: u16,
    pub ime: u16,
}

impl Mmu {

    pub fn trigger_dma(&mut self, channel: usize) {
        println!("DMA {} triggered! SAD={:08X} DAD={:08X} count={}", channel, self.dma[channel].sad, self.dma[channel].dad, self.dma[channel].count);
        let sad = self.dma[channel].sad;
        let dad = self.dma[channel].dad;
        let count = if self.dma[channel].count == 0 {
            if channel == 3 { 0x10000 } else { 0x4000 }
        } else {
            self.dma[channel].count as u32
        };
        let ctrl = self.dma[channel].ctrl;
        
        let timing = (ctrl >> 12) & 3;
        if timing != 0 {
            return;
        }

        let is_32bit = (ctrl & (1 << 10)) != 0;
        let src_ctrl = (ctrl >> 7) & 3;
        let dst_ctrl = (ctrl >> 5) & 3;

        let mut s = sad;
        let mut d = dad;
        
        for _ in 0..count {
            if is_32bit {
                let val = self.read32(s);
                self.write32(d, val);
                match src_ctrl {
                    0 => s = s.wrapping_add(4),
                    1 => s = s.wrapping_sub(4),
                    _ => {}
                }
                match dst_ctrl {
                    0 | 3 => d = d.wrapping_add(4),
                    1 => d = d.wrapping_sub(4),
                    _ => {}
                }
            } else {
                let val = self.read16(s);
                self.write16(d, val);
                match src_ctrl {
                    0 => s = s.wrapping_add(2),
                    1 => s = s.wrapping_sub(2),
                    _ => {}
                }
                match dst_ctrl {
                    0 | 3 => d = d.wrapping_add(2),
                    1 => d = d.wrapping_sub(2),
                    _ => {}
                }
            }
        }
        
        self.dma[channel].ctrl &= !(1 << 15);
    }

    pub fn new() -> Self {
        Self {
            bios: include_bytes!("../../spec/gba_bios_stub.bin").to_vec(),
            ewram: Box::new([0; 256 * 1024]),
            iwram: Box::new([0; 32 * 1024]),
            rom: vec![0; 32 * 1024 * 1024],
            sram: Box::new([0; 64 * 1024]),
            ppu: Ppu::new(),
            dma: [DmaChannel::new(); 4],
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
            0x04 => { if addr != 0x04000208 && addr != 0x04000209 && addr != 0x0400020A && addr != 0x0400020B { println!("IO Write {:08X}={:02X}", addr, val); } println!("IO Write {:08X}={:02X}", addr, val);
                match addr & 0xFFFFFF {
                    0x200 => self.ie = (self.ie & 0xFF00) | (val as u16),
                    0x201 => self.ie = (self.ie & 0x00FF) | ((val as u16) << 8),
                    0x202 => self.i_f &= !(val as u16),
                    0x203 => self.i_f &= !((val as u16) << 8),
                    0x208 => self.ime = (self.ime & 0xFF00) | (val as u16),
                    0x209 => self.ime = (self.ime & 0x00FF) | ((val as u16) << 8),

                    0x0B0 => self.dma[0].sad = (self.dma[0].sad & 0xFFFFFF00) | (val as u32),
                    0x0B1 => self.dma[0].sad = (self.dma[0].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0B2 => self.dma[0].sad = (self.dma[0].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0B3 => self.dma[0].sad = (self.dma[0].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0B4 => self.dma[0].dad = (self.dma[0].dad & 0xFFFFFF00) | (val as u32),
                    0x0B5 => self.dma[0].dad = (self.dma[0].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0B6 => self.dma[0].dad = (self.dma[0].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0B7 => self.dma[0].dad = (self.dma[0].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0B8 => self.dma[0].count = (self.dma[0].count & 0xFF00) | (val as u16),
                    0x0B9 => self.dma[0].count = (self.dma[0].count & 0x00FF) | ((val as u16) << 8),
                    0x0BA => self.dma[0].ctrl = (self.dma[0].ctrl & 0xFF00) | (val as u16),
                    0x0BB => {
                        self.dma[0].ctrl = (self.dma[0].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(0); }
                    }

                    0x0BC => self.dma[1].sad = (self.dma[1].sad & 0xFFFFFF00) | (val as u32),
                    0x0BD => self.dma[1].sad = (self.dma[1].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0BE => self.dma[1].sad = (self.dma[1].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0BF => self.dma[1].sad = (self.dma[1].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0C0 => self.dma[1].dad = (self.dma[1].dad & 0xFFFFFF00) | (val as u32),
                    0x0C1 => self.dma[1].dad = (self.dma[1].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0C2 => self.dma[1].dad = (self.dma[1].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0C3 => self.dma[1].dad = (self.dma[1].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0C4 => self.dma[1].count = (self.dma[1].count & 0xFF00) | (val as u16),
                    0x0C5 => self.dma[1].count = (self.dma[1].count & 0x00FF) | ((val as u16) << 8),
                    0x0C6 => self.dma[1].ctrl = (self.dma[1].ctrl & 0xFF00) | (val as u16),
                    0x0C7 => {
                        self.dma[1].ctrl = (self.dma[1].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(1); }
                    }

                    0x0C8 => self.dma[2].sad = (self.dma[2].sad & 0xFFFFFF00) | (val as u32),
                    0x0C9 => self.dma[2].sad = (self.dma[2].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0CA => self.dma[2].sad = (self.dma[2].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0CB => self.dma[2].sad = (self.dma[2].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0CC => self.dma[2].dad = (self.dma[2].dad & 0xFFFFFF00) | (val as u32),
                    0x0CD => self.dma[2].dad = (self.dma[2].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0CE => self.dma[2].dad = (self.dma[2].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0CF => self.dma[2].dad = (self.dma[2].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0D0 => self.dma[2].count = (self.dma[2].count & 0xFF00) | (val as u16),
                    0x0D1 => self.dma[2].count = (self.dma[2].count & 0x00FF) | ((val as u16) << 8),
                    0x0D2 => self.dma[2].ctrl = (self.dma[2].ctrl & 0xFF00) | (val as u16),
                    0x0D3 => {
                        self.dma[2].ctrl = (self.dma[2].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(2); }
                    }

                    0x0D4 => self.dma[3].sad = (self.dma[3].sad & 0xFFFFFF00) | (val as u32),
                    0x0D5 => self.dma[3].sad = (self.dma[3].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0D6 => self.dma[3].sad = (self.dma[3].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0D7 => self.dma[3].sad = (self.dma[3].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0D8 => self.dma[3].dad = (self.dma[3].dad & 0xFFFFFF00) | (val as u32),
                    0x0D9 => self.dma[3].dad = (self.dma[3].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0DA => self.dma[3].dad = (self.dma[3].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0DB => self.dma[3].dad = (self.dma[3].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0DC => self.dma[3].count = (self.dma[3].count & 0xFF00) | (val as u16),
                    0x0DD => self.dma[3].count = (self.dma[3].count & 0x00FF) | ((val as u16) << 8),
                    0x0DE => self.dma[3].ctrl = (self.dma[3].ctrl & 0xFF00) | (val as u16),
                    0x0DF => {
                        self.dma[3].ctrl = (self.dma[3].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(3); }
                    }



                    _ => self.ppu.write8(addr, val),
                }
            },
            0x05 => self.ppu.palette[(addr & 0x3FF) as usize] = val,
            0x06 => {
                let offset = addr & 0x1FFFF;
                if offset < 96 * 1024 {
                    self.ppu.vram[offset as usize] = val; println!("VRAM write {:08X}={:02X}", offset, val);
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
