import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if pc == 0x08000178 { println!("REACHED 08000178!"); }', 'if pc == 0x0800016C { println!("REACHED 0800016C!"); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
