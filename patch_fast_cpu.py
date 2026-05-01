import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('        let cycles = match pc >> 24 {\n            0x02 => if self.get_t() { 3 } else { 6 },\n            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => 4, // ROM\n            0x0E => 5,\n            _ => 1,\n        };\n        self.cycles += cycles;', '        self.cycles += 1;')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
