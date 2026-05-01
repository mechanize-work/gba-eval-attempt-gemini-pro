import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if true_pc >= 0x08000220 && true_pc <= 0x08000240 { println!("Trace: PC={:08X}"', 'if cycle_count % 1000000 == 0 { println!("Trace: cycle {} PC={:08X}", cycle_count')

with open("tests/compare.rs", "w") as f:
    f.write(src)
