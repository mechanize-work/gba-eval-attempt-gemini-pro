import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

stm_fix = """    fn execute_thumb_multiple_load_store(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let rb = ((instr >> 8) & 0x7) as usize;
        let r_list = instr & 0xFF;

        let mut addr = self.regs[rb];
        let mut empty_rlist = false;
        
        let list = if r_list == 0 {
            empty_rlist = true;
            1 << 15
        } else {
            r_list as u32
        };

        for i in 0..16 {
            if (list & (1 << i)) != 0 {
                if l_bit { // LDMIA
                    self.regs[i] = bus.read32(addr);
                } else { // STMIA
                    let val = if i == 15 { self.regs[15].wrapping_add(2) } else { self.regs[i] };
                    bus.write32(addr, val);
                }
                addr += 4;
            }
        }
        
        let writeback = !l_bit || (r_list & (1 << rb)) == 0;
        if writeback {
            self.regs[rb] = if empty_rlist { self.regs[rb].wrapping_add(0x40) } else { addr };
        }
    }"""

start = src.find("fn execute_thumb_multiple_load_store")
end = src.find("}", src.find("self.regs[rb] = addr;", start)) + 1
src = src[:start] + stm_fix + src[end+1:]

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
