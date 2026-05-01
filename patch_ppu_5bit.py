import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

src = src.replace('final_r = ((final_r * eva + old_r * evb) / 16).min(255);',
                  'final_r = ((((final_r >> 3) * eva + (old_r >> 3) * evb) / 16).min(31) << 3) | ((((final_r >> 3) * eva + (old_r >> 3) * evb) / 16).min(31) >> 2);')
src = src.replace('final_g = ((final_g * eva + old_g * evb) / 16).min(255);',
                  'final_g = ((((final_g >> 3) * eva + (old_g >> 3) * evb) / 16).min(31) << 3) | ((((final_g >> 3) * eva + (old_g >> 3) * evb) / 16).min(31) >> 2);')
src = src.replace('final_b = ((final_b * eva + old_b * evb) / 16).min(255);',
                  'final_b = ((((final_b >> 3) * eva + (old_b >> 3) * evb) / 16).min(31) << 3) | ((((final_b >> 3) * eva + (old_b >> 3) * evb) / 16).min(31) >> 2);')

with open("src/ppu/mod.rs", "w") as f:
    f.write(src)
