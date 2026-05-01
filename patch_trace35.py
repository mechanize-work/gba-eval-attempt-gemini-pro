import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if diff_count < 10 { println!("Frame {}', 'if diff_count == 0 { println!("PAL0: {:02X}{:02X}", gba_mut().mmu.ppu.palette[1], gba_mut().mmu.ppu.palette[0]); }\n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
