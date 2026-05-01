import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'if _cycle_count % 1000000 == 0 { println!("PC={:08X} count={}", gba_mut().cpu.regs[15], _cycle_count); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
