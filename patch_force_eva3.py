import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

src = src.replace('let eva = (self.bldalpha & 0x1F).min(16) as u32;', 'let eva = 13;')

with open("src/ppu/mod.rs", "w") as f:
    f.write(src)
