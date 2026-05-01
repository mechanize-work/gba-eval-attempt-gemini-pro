import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('            0x05 => { // VBlankIntrWait\n                bus.write8(0x04000202, 1); // Clear VBlank IF\n                self.halted = true;\n                true\n            }',
                  '            0x05 => { // VBlankIntrWait\n                println!("SWI 5 CALLED at cycle {}", self.cycles);\n                bus.write8(0x04000202, 1); // Clear VBlank IF\n                self.halted = true;\n                true\n            }')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
