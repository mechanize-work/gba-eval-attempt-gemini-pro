import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if cycle_count < 100 { println!("Trace: PC={:08X}', 'if true_pc >= 0x08000220 && true_pc <= 0x08000240 { println!("Trace: PC={:08X}')

with open("tests/compare.rs", "w") as f:
    f.write(src)
