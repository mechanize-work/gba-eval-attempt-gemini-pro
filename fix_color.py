import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

def repl(text):
    return text.replace("let pr = (c & 0x1F) << 3;\n                                let pg = ((c >> 5) & 0x1F) << 3;\n                                let pb = ((c >> 10) & 0x1F) << 3;", "let r = c & 0x1F;\n                                let g = (c >> 5) & 0x1F;\n                                let b = (c >> 10) & 0x1F;\n                                let pr = (r << 3) | (r >> 2);\n                                let pg = (g << 3) | (g >> 2);\n                                let pb = (b << 3) | (b >> 2);")

new_src = repl(src)

new_src = new_src.replace("let r = (c0 & 0x1F) << 3;\n        let g = ((c0 >> 5) & 0x1F) << 3;\n        let b = ((c0 >> 10) & 0x1F) << 3;", "let r0 = c0 & 0x1F;\n        let g0 = (c0 >> 5) & 0x1F;\n        let b0 = (c0 >> 10) & 0x1F;\n        let r = (r0 << 3) | (r0 >> 2);\n        let g = (g0 << 3) | (g0 >> 2);\n        let b = (b0 << 3) | (b0 >> 2);")

with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
