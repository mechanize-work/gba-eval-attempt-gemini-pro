import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('println!("SWI {:02X} CALLED! i_f=', 'println!("ANY SWI {:02X} CALLED! i_f=', 1)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
