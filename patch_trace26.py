import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Diff at', 'if diff_count == 0 { println!("DISPCNT: {:04X}", gba_mut().mmu.ppu.dispcnt); }\n        println!("Diff at')

with open("tests/compare.rs", "w") as f:
    f.write(src)
