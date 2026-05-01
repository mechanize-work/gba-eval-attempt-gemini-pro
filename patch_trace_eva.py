import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("End of frame {}: PC={:08X}", i, gba_mut().cpu.regs[15]);', 'println!("End of frame {}: PC={:08X} EVA={}", i, gba_mut().cpu.regs[15], gba_mut().mmu.ppu.bldalpha & 0x1F);')

with open("tests/compare.rs", "w") as f:
    f.write(src)
