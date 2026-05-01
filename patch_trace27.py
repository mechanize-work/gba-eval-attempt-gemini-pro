import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Frame 1 differences:', 'for i in 256..512 { let c = (gba_mut().mmu.ppu.palette[i*2] as u16) | ((gba_mut().mmu.ppu.palette[i*2+1] as u16) << 8); if c == 0x0000 { println!("OBJ PAL 0000 at index {}", i); } }\n        println!("Frame 1 differences:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
