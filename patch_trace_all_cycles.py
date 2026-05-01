import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if count_a == 1 { println!("EVA WRITTEN: {} at cycle {}", gba_mut().mmu.ppu.bldalpha & 0x1F, gba_mut().cpu.cycles); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
