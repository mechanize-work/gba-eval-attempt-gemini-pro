import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

waitcnt_logic = """
    pub fn get_memory_cycles_32(&self, addr: u32, waitcnt: u16) -> usize {
        match addr >> 24 {
            0x02 => { // EWRAM
                let wait = match (waitcnt >> 24) & 0xF {
                    _ => 3 // Waitcnt bits 24..27 are for waitstate 2... actually ewram wait is bits 24-27 of memory control?
                    // Actually GBA EWRAM waitstate is 256K, fixed at 3 waitstates in waitcnt? No, WAITCNT is 0x4000204.
                    // Let's stick to 3.
                };
                3
            },
            0x08 | 0x09 => { // ROM Wait State 0
                let s_wait = match (waitcnt >> 4) & 1 { 0 => 2, 1 => 1, _ => 1 };
                let n_wait = match (waitcnt >> 2) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                // Approximate 32-bit read as N + S
                n_wait + s_wait
            },
            0x0A | 0x0B => { // ROM Wait State 1
                let s_wait = match (waitcnt >> 7) & 1 { 0 => 4, 1 => 1, _ => 1 };
                let n_wait = match (waitcnt >> 5) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                n_wait + s_wait
            },
            0x0C | 0x0D => { // ROM Wait State 2
                let s_wait = match (waitcnt >> 10) & 1 { 0 => 8, 1 => 1, _ => 1 };
                let n_wait = match (waitcnt >> 8) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                n_wait + s_wait
            },
            0x0E => { // SRAM
                let wait = match waitcnt & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                wait
            },
            _ => 1,
        }
    }

    pub fn get_memory_cycles_16(&self, addr: u32, waitcnt: u16) -> usize {
        match addr >> 24 {
            0x02 => 3, // EWRAM
            0x08 | 0x09 => { // ROM Wait State 0
                let n_wait = match (waitcnt >> 2) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                n_wait // approximate 16-bit as N
            },
            0x0A | 0x0B => { // ROM Wait State 1
                let n_wait = match (waitcnt >> 5) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                n_wait
            },
            0x0C | 0x0D => { // ROM Wait State 2
                let n_wait = match (waitcnt >> 8) & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 };
                n_wait
            },
            0x0E => match waitcnt & 3 { 0 => 4, 1 => 3, 2 => 2, 3 => 8, _ => 4 },
            _ => 1,
        }
    }
"""

src = src.replace('pub fn get_memory_cycles_32(&self, addr: u32) -> usize {\n        match addr >> 24 {\n            0x02 => 3, // EWRAM\n            0x03 => 1, // IWRAM\n            0x04 => 1, // I/O\n            0x05 => 1, // PAL\n            0x06 => 1, // VRAM\n            0x07 => 1, // OAM\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => 4, // ROM\n            0x0E => 5, // SRAM\n            _ => 1,\n        }\n    }', waitcnt_logic)

import re

# Fix step cycles to read WAITCNT via bus... wait, cpu doesn't have direct access.
# Let's add waitcnt to CPU.
src = src.replace('    pub cycles: usize,\n    pub halted: bool,\n    pub saved_ime: u16,\n}', '    pub cycles: usize,\n    pub halted: bool,\n    pub saved_ime: u16,\n    pub waitcnt: u16,\n}')
src = src.replace('            halted: false,\n            saved_ime: 0xFFFF,\n        }', '            halted: false,\n            saved_ime: 0xFFFF,\n            waitcnt: 0,\n        }')

new_step = """        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });
        let cycles = if self.get_t() {
            self.get_memory_cycles_16(pc, self.waitcnt)
        } else {
            self.get_memory_cycles_32(pc, self.waitcnt)
        };
        self.cycles += cycles;"""

src = re.sub(r'        let pc = self\.regs\[15\]\.wrapping_sub.*?self\.cycles \+= 1;', new_step, src, flags=re.DOTALL)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)


with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cpu.step(&mut self.mmu);', 'self.cpu.waitcnt = self.mmu.waitcnt;\n        self.cpu.step(&mut self.mmu);')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)

