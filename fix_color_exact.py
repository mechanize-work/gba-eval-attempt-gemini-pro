import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

# Mesen RGB mapping:
# Let's map back. Em=(0,0,0) Ref=(16,33,24)
# What if the background color should be extracted exactly like the reference?
# If we simply shift by 3: (16 >> 3, 33 >> 3, 24 >> 3) -> (2, 4, 3)
# 2 << 3 = 16.
# 4 << 3 = 32. But ref is 33! Why?
# In Mesen: output = (color * 255) / 31.
# 2 * 255 / 31 = 510 / 31 = 16.45 => 16.
# 4 * 255 / 31 = 1020 / 31 = 32.9 => 33.
# 3 * 255 / 31 = 765 / 31 = 24.67 => 24.
# Exactly! Mesen uses `(c * 255 + 15) / 31`.
# Let's implement EXACTLY THIS!
def repl(text):
    return text.replace("let pr = (r << 3) | (r >> 2);\n                                let pg = (g << 3) | (g >> 2);\n                                let pb = (b << 3) | (b >> 2);", "let pr = ((r as u32 * 255 + 15) / 31) as u8;\n                                let pg = ((g as u32 * 255 + 15) / 31) as u8;\n                                let pb = ((b as u32 * 255 + 15) / 31) as u8;")

new_src = repl(src)

new_src = new_src.replace("let r = (r0 << 3) | (r0 >> 2);\n        let g = (g0 << 3) | (g0 >> 2);\n        let b = (b0 << 3) | (b0 >> 2);", "let r = ((r0 as u32 * 255 + 15) / 31) as u8;\n        let g = ((g0 as u32 * 255 + 15) / 31) as u8;\n        let b = ((b0 as u32 * 255 + 15) / 31) as u8;")

with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
