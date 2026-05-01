import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        self.cycles += 1;\n\n        if self.get_t() {', '        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });\n        let cycles = match pc >> 24 {\n            0x02 => if self.get_t() { 6 } else { 12 },\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => if self.get_t() { 10 } else { 20 },\n            0x0E => 20,\n            _ => 2,\n        };\n        self.cycles += cycles;\n\n        if self.get_t() {')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
