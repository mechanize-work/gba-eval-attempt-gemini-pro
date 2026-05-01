import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count < 10 {', 'if diff_count == 0 { println!("BLDCNT={:04X} BLDALPHA={:04X}", gba_mut().mmu.ppu.bldcnt, gba_mut().mmu.ppu.bldalpha); }\n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
