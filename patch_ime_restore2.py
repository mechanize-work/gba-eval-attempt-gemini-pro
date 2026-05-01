import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('pub cycles: usize,\n    pub halted: bool,\n}', 'pub cycles: usize,\n    pub halted: bool,\n    pub saved_ime: u16,\n}')
src = src.replace('cycles: 0,\n            halted: false,\n        }', 'cycles: 0,\n            halted: false,\n            saved_ime: 0xFFFF,\n        }')

src = src.replace('bus.write16(0x04000208, 1); // Set IME=1\n                self.halted = true;', 'self.saved_ime = bus.read16(0x04000208);\n                bus.write16(0x04000208, 1); // Set IME=1\n                self.halted = true;')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cpu.halted = false;\n            }\n            if self.mmu.ime != 0 && (self.mmu.ie & self.mmu.i_f) != 0 {', 'self.cpu.halted = false;\n                if self.cpu.saved_ime != 0xFFFF {\n                    self.mmu.ime = self.cpu.saved_ime;\n                    self.cpu.saved_ime = 0xFFFF;\n                }\n            }\n            if self.mmu.ime != 0 && (self.mmu.ie & self.mmu.i_f) != 0 {')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
