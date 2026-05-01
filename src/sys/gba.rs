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

    pub fn step(&mut self, framebuffer: &mut [u32; 240 * 160]) {
        
        // IRQ logic
        if self.mmu.ime != 0 {
            if (self.mmu.ie & self.mmu.i_f) != 0 {
                self.cpu.trigger_irq(); println!("VBlank IRQ Triggered! IE={:04X} IF={:04X}", self.mmu.ie, self.mmu.i_f);
            }
        }

        self.cpu.step(&mut self.mmu);
        // Assuming 1 instruction = 1 cycle for now, very inaccurate.
        self.cycles += 1;

        // PPU timings: 1 line = 1232 cycles (actually 960 active, 272 hblank)
        if self.cycles >= 1232 {
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
            if self.mmu.ime != 0 && (self.mmu.ie & self.mmu.i_f) != 0 {
                // Trigger IRQ exception
                let old_cpsr = self.cpu.cpsr;
                self.cpu.set_mode(crate::cpu::arm7tdmi::Mode::Irq);
                self.cpu.spsr = old_cpsr;
                self.cpu.regs[14] = self.cpu.regs[15]; // Not wrapping_add 4 since we are currently executing
                self.cpu.set_t(false);
                self.cpu.set_i(true);
                self.cpu.regs[15] = 0x00000018;
                self.cpu.reload_pipeline();
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
