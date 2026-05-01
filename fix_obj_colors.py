import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

def repl(text):
    text = text.replace("let pr = (c & 0x1F) << 3;\n                                            let pg = ((c >> 5) & 0x1F) << 3;\n                                            let pb = ((c >> 10) & 0x1F) << 3;\n                                            framebuffer[start + screen_x as usize] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);", "let r = c & 0x1F;\n                                            let g = (c >> 5) & 0x1F;\n                                            let b = (c >> 10) & 0x1F;\n                                            let pr = (r << 3) | (r >> 2);\n                                            let pg = (g << 3) | (g >> 2);\n                                            let pb = (b << 3) | (b >> 2);\n                                            framebuffer[start + screen_x as usize] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);")
    return text

new_src = repl(src)
print("Replaced" if new_src != src else "Unchanged")
with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
