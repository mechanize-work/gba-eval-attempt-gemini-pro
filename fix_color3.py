import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

def repl(text):
    return text.replace("let color = 0xFF000000 | ((b as u32) << 16) | ((g as u32) << 8) | (r as u32);", "let color = 0xFF000000 | ((b as u32) << 16) | ((g as u32) << 8) | (r as u32);")

new_src = repl(src)

new_src = new_src.replace("let pr = (r << 3) | (r >> 2);\n                                let pg = (g << 3) | (g >> 2);\n                                let pb = (b << 3) | (b >> 2);", "let pr = (r << 3) | (r >> 2);\n                                let pg = (g << 3) | (g >> 2);\n                                let pb = (b << 3) | (b >> 2);")

new_src = new_src.replace("let r = (r0 << 3) | (r0 >> 2);\n        let g = (g0 << 3) | (g0 >> 2);\n        let b = (b0 << 3) | (b0 >> 2);", "let r = (r0 << 3) | (r0 >> 2);\n        let g = (g0 << 3) | (g0 >> 2);\n        let b = (b0 << 3) | (b0 >> 2);")

with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
