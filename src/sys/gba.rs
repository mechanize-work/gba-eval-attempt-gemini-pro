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
        if self.cycles < 50 * 4 {
            // println!("PC: {:08X}", self.cpu.regs[15]);
        }
        self.cpu.step(&mut self.mmu);
        // Assuming 1 instruction = 1 cycle for now, very inaccurate.
        // Or wait, let's step 4 cycles per instruction for now.
        self.cycles += 4;
        
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
                // TODO: trigger irq if enabled
            } else {
                self.mmu.ppu.dispstat &= !(1 << 2);
            }
            
            // vblank flag
            if next_line >= 160 && next_line <= 226 {
                self.mmu.ppu.dispstat |= 1;
            } else {
                self.mmu.ppu.dispstat &= !1;
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
