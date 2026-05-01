import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

timer_code = """
        // Tick timers
        let mut previous_overflow = false;
        for i in 0..4 {
            let control = self.mmu.timers[i].control;
            if (control & 0x80) != 0 {
                let is_cascade = (control & 0x04) != 0;
                let mut ticked = false;
                
                if is_cascade {
                    if previous_overflow {
                        ticked = true;
                    }
                } else {
                    let prescaler_shift = match control & 3 {
                        0 => 0,
                        1 => 6,
                        2 => 8,
                        3 => 10,
                        _ => 0,
                    };
                    let prescaler = 1 << prescaler_shift;
                    // Simplification: just add elapsed cycles, maybe inaccurate sub-cycle timing
                    let old_counter = self.mmu.timers[i].counter;
                    let new_counter = old_counter + (elapsed as u32);
                    self.mmu.timers[i].counter = new_counter;
                    
                    if (new_counter >> prescaler_shift) > (old_counter >> prescaler_shift) {
                        ticked = true;
                    }
                }
                
                previous_overflow = false;
                if ticked {
                    // It actually ticks the 16-bit timer by 1
                    let val = (self.mmu.timers[i].counter >> 16) as u16; // wait, this is wrong.
                }
            } else {
                previous_overflow = false;
            }
        }
"""

src = src.replace('        let elapsed = self.cpu.cycles - start_cycles;\n        self.cycles += elapsed;', '        let elapsed = self.cpu.cycles - start_cycles;\n        self.cycles += elapsed;\n        self.tick_timers(elapsed);')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
