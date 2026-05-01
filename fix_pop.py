import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""        if l_bit { // POP
            let mut addr = self.regs[13];
            for i in 0..8 {
                if (r_list & (1 << i)) != 0 {
                    self.regs[i] = bus.read32(addr);
                    addr += 4;
                }
            }
            if r_bit {
                let val = bus.read32(addr);
                self.regs[15] = val & !1;
                self.set_t((val & 1) != 0);
                self.reload_pipeline();
                addr += 4;
            }
            self.regs[13] = addr;""", """        if l_bit { // POP
            let mut addr = self.regs[13];
            for i in 0..8 {
                if (r_list & (1 << i)) != 0 {
                    self.regs[i] = bus.read32(addr);
                    addr += 4;
                }
            }
            if r_bit {
                let val = bus.read32(addr);
                self.regs[15] = val & !1;
                // Wait, POP PC shouldn't change T bit usually? 
                // Ah, ARMv5T says POP to PC can switch state. Wait, yes, it sets T bit based on LSB.
                self.set_t((val & 1) != 0);
                self.reload_pipeline();
                addr += 4;
            }
            self.regs[13] = addr;""")
print("Replaced" if new_src != src else "Unchanged")
