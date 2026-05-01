import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count < 10 {', 'if diff_count < 5 { println!("Diff at {}: target1={} target2={} effect={} eva={} evb={}", i, gba_mut().mmu.ppu.bldcnt & 0x3F, (gba_mut().mmu.ppu.bldcnt >> 8) & 0x3F, (gba_mut().mmu.ppu.bldcnt >> 6) & 3, gba_mut().mmu.ppu.bldalpha & 0x1F, (gba_mut().mmu.ppu.bldalpha >> 8) & 0x1F); }\n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
