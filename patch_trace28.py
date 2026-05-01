import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if c == 0x0000 { println!("OBJ PAL 0000 at index {}", i); }', 'if c == 0x0000 && i % 16 != 0 { println!("OBJ PAL 0000 at index {}", i); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
