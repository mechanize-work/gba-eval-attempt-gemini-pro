import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('            0x05 => { // VBlankIntrWait\n                self.halted = true;\n                true\n            }',
                  '            0x05 => { // VBlankIntrWait\n                bus.write8(0x04000202, 1); // Clear VBlank IF\n                self.halted = true;\n                true\n            }')

src = src.replace('            0x04 => { // IntrWait\n                self.halted = true;\n                true\n            }',
                  '            0x04 => { // IntrWait\n                let wait_flags = self.regs[1];\n                bus.write16(0x04000202, wait_flags as u16); // Clear waited IF\n                self.halted = true;\n                true\n            }')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
