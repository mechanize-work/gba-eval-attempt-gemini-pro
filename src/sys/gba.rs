use crate::cpu::arm7tdmi::Cpu;
use crate::memory::mmu::Mmu;

pub struct Gba {
    pub cpu: Cpu,
    pub mmu: Mmu,
    pub cycles: usize,
}

impl Gba {
    pub fn new() -> Self {
        Self {
            cpu: Cpu::new(),
            mmu: Mmu::new(),
            cycles: 0,
        }
    }

    pub fn reset(&mut self) {
        self.cpu = Cpu::new();
        self.cpu.regs[15] = 0x00000000;
        self.cpu.pipeline_empty = true;
        self.cycles = 0;
    }

    
    fn tick_timers(&mut self, elapsed: usize) {
        let mut previous_overflow = false;
        for i in 0..4 {
            let control = self.mmu.timers[i].control;
            let mut current_overflow = false;
            if (control & 0x80) != 0 {
                let is_cascade = (control & 0x04) != 0 && i > 0;
                let mut ticks = 0;
                
                if is_cascade {
                    if previous_overflow {
                        ticks = 1;
                    }
                } else {
                    let prescaler_shift = match control & 3 {
                        0 => 0,
                        1 => 6,
                        2 => 8,
                        3 => 10,
                        _ => 0,
                    };
                    let prescaler_mask = (1 << prescaler_shift) - 1;
                    let old_ticks = self.mmu.timers[i].counter & prescaler_mask;
                    let new_ticks = old_ticks + (elapsed as u32);
                    ticks = new_ticks >> prescaler_shift;
                    self.mmu.timers[i].counter = (self.mmu.timers[i].counter & !prescaler_mask) | (new_ticks & prescaler_mask);
                }
                
                if ticks > 0 {
                    let old_val = (self.mmu.timers[i].counter >> 16) as u32;
                    let new_val = old_val + ticks;
                    if new_val >= 0x10000 {
                        current_overflow = true;
                        let reload = self.mmu.timers[i].reload as u32;
                        let overflow_count = new_val - 0x10000;
                        let final_val = reload + (overflow_count % (0x10000 - reload));
                        self.mmu.timers[i].counter = (self.mmu.timers[i].counter & 0xFFFF) | (final_val << 16);
                        
                        // IRQ
                        if (control & 0x40) != 0 {
                            println!("TIMER {} IRQ at cycle {}!", i, self.cpu.cycles);
                            self.mmu.i_f |= 1 << (3 + i);
                        }
                    } else {
                        self.mmu.timers[i].counter = (self.mmu.timers[i].counter & 0xFFFF) | (new_val << 16);
                    }
                }
            }
            previous_overflow = current_overflow;
        }
    }

    pub fn step(&mut self, framebuffer: &mut [u32; 240 * 160]) {
        let start_cycles = self.cpu.cycles;
        self.cpu.step(&mut self.mmu);
        let elapsed = self.cpu.cycles - start_cycles;
        self.cycles += elapsed;
        self.tick_timers(elapsed);

        // PPU timings: 1 line = 1232 cycles (actually 960 active, 272 hblank)
        while self.cycles >= 1232 {
            self.cycles -= 1232;
            let current_line = self.mmu.ppu.vcount;
            
            // If in visible area, render it
            if current_line < 160 {
                self.mmu.ppu.render_scanline(framebuffer, current_line as usize);
            }
            
            let mut next_line = current_line + 1;
            if next_line >= 228 {
                next_line = 0;
            }
            
            self.mmu.ppu.vcount = next_line;
            // update dispstat vcount flag
            let vcount_setting = (self.mmu.ppu.dispstat >> 8) & 0xFF;
            if next_line == vcount_setting {
                self.mmu.ppu.dispstat |= 1 << 2; // vcounter flag
                if (self.mmu.ppu.dispstat & (1 << 5)) != 0 {
                    self.mmu.i_f |= 1 << 2; // V-Counter IRQ
                }
            } else {
                self.mmu.ppu.dispstat &= !(1 << 2);
            }
            
            // vblank flag
            if next_line >= 160 && next_line <= 226 {
                if next_line == 160 {
                    self.mmu.ppu.dispstat |= 1;
                    if (self.mmu.ppu.dispstat & (1 << 3)) != 0 {
                        self.mmu.i_f |= 1 << 0; // V-Blank IRQ
                    }
                }
            } else {
                self.mmu.ppu.dispstat &= !1;
            }

            // check if IRQ should be processed
            
            if (self.mmu.ie & self.mmu.i_f) != 0 {
                let was_halted = self.cpu.halted;
                self.cpu.halted = false;
                


                if self.mmu.ime != 0 && (self.cpu.cpsr & 0x80) == 0 {
                    // Trigger IRQ exception
                    let old_cpsr = self.cpu.cpsr;
                    self.cpu.set_mode(crate::cpu::arm7tdmi::Mode::Irq);
                    self.cpu.spsr = old_cpsr;
                    
                    self.cpu.regs[14] = if was_halted {
                        self.cpu.regs[15].wrapping_sub(if self.cpu.get_t() { 2 } else { 4 })
                    } else if self.cpu.pipeline_empty {
                        self.cpu.regs[15].wrapping_add(4)
                    } else if self.cpu.get_t() {
                        self.cpu.regs[15].wrapping_add(2)
                    } else {
                        self.cpu.regs[15]
                    };
                    
                    self.cpu.set_t(false);
                    self.cpu.set_i(true);
                    self.cpu.regs[15] = 0x00000018;
                    self.cpu.reload_pipeline();
                }
            }

        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bios_execution() {
        let mut gba = Gba::new();
        let bios = include_bytes!("../../spec/gba_bios_stub.bin");
        gba.mmu.bios[..bios.len()].copy_from_slice(bios);
        gba.reset();
        
        let mut fb = [0; 240 * 160];

        for _i in 0..20 {
            gba.step(&mut fb);
        }
    }
}
