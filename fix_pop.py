import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""            if r_bit {
                let val = bus.read32(addr);
                self.regs[15] = val & !1;
                self.set_t((val & 1) != 0);
                self.reload_pipeline();
                addr += 4;
            }""", """            if r_bit {
                let val = bus.read32(addr);
                // When popping PC, bit 0 is ignored for PC value, but it sets the T bit!
                self.regs[15] = val & !1;
                self.set_t((val & 1) != 0);
                self.reload_pipeline();
                addr += 4;
            }""")
print("Replaced" if new_src != src else "Unchanged")
