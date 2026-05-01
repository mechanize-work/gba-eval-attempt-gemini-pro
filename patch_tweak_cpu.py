import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        let cycles = match pc >> 24 {\n            0x02 => if self.get_t() { 3 } else { 6 },\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => if self.get_t() { 1 } else { 2 }, // Prefetch buffer speeds this up significantly\n            0x0E => 5,\n            _ => 1,\n        };\n        self.cycles += cycles;', '        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        let cycles = match pc >> 24 {\n            0x02 => if self.get_t() { 3 } else { 6 },\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => if self.get_t() { 2 } else { 4 },\n            0x0E => 5,\n            _ => 1,\n        };\n        self.cycles += cycles;')

src = src.replace('self.cycles += 1;\n\n        if self.get_t() {', 'let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        let cycles = match pc >> 24 {\n            0x02 => if self.get_t() { 3 } else { 6 },\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => if self.get_t() { 2 } else { 4 },\n            0x0E => 5,\n            _ => 1,\n        };\n        self.cycles += cycles;\n\n        if self.get_t() {')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
