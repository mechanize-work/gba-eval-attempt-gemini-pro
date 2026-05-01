import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

def repl(text):
    return text.replace("let color = 0xFF000000 | (b << 16) | (g << 8) | r;", "let color = 0xFF000000 | ((b as u32) << 16) | ((g as u32) << 8) | (r as u32);")

new_src = repl(src)

with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
