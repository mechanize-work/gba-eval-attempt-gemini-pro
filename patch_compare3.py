import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Frame 60 done: PC={:08X}", gba_mut().cpu.regs[15]);',
                  'for fb_frame in 1..=60 { println!("Frame {} ended at PC={:08X}", fb_frame, gba_mut().cpu.regs[15]); }')
src = src.replace('for i in 0..60 {', 'for i in 0..60 {\n            println!("End of frame {}: PC={:08X}", i, gba_mut().cpu.regs[15]);')

with open("tests/compare.rs", "w") as f:
    f.write(src)
