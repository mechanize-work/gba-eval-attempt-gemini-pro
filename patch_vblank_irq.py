import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'// Check VBLANK IRQ\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n.*?\n', '', src)

new_vcount = """
            if current_line == 160 {
                self.mmu.ppu.dispstat |= 1;
                // VBlank IRQ
                if (self.mmu.ppu.dispstat & 8) != 0 {
                    self.mmu.i_f |= 1;
                }
            }
"""
src = src.replace('if current_line == 160 {\n                self.mmu.ppu.dispstat |= 1;\n            }', new_vcount)

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
