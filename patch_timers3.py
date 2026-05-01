import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

timer_fn = """
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
"""

src = src.replace('pub fn step(&mut self, framebuffer: &mut [u32; 240 * 160]) {', timer_fn + '\n    pub fn step(&mut self, framebuffer: &mut [u32; 240 * 160]) {')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
