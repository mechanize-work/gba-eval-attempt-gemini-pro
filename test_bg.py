import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

new_src = src.replace("""                                let pr = ((r as u32 * 255 + 15) / 31) as u8;
                                let pg = ((g as u32 * 255 + 15) / 31) as u8;
                                let pb = ((b as u32 * 255 + 15) / 31) as u8;""", """                                let pr = (r << 3) | (r >> 2);
                                let pg = (g << 3) | (g >> 2);
                                let pb = (b << 3) | (b >> 2);""")

new_src = new_src.replace("""        let r = ((r0 as u32 * 255 + 15) / 31) as u8;
        let g = ((g0 as u32 * 255 + 15) / 31) as u8;
        let b = ((b0 as u32 * 255 + 15) / 31) as u8;""", """        let r = (r0 << 3) | (r0 >> 2);
        let g = (g0 << 3) | (g0 >> 2);
        let b = (b0 << 3) | (b0 >> 2);""")
with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
