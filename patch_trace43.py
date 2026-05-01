import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if (gba_mut().mmu.ppu.bldalpha & 0x1F) != 0 { println!("EVA={} at PC={:08X}", gba_mut().mmu.ppu.bldalpha & 0x1F, gba_mut().cpu.regs[15]); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
