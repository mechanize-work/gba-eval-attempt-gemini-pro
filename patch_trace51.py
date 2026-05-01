import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('println!("SWI {:02X} CALLED", swi_num);', 'println!("SWI {:02X} CALLED! i_f={:04X} ie={:04X} ime={:04X}", swi_num, bus.read16(0x04000202), bus.read16(0x04000200), bus.read16(0x04000208));')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
