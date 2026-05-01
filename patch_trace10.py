import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if pc == 0x0800016C { println!("MEMCPY ARGS', 'if pc == 0x0800014A || pc == 0x08000154 || pc == 0x0800016C { println!("MEMCPY ARGS')

with open("tests/compare.rs", "w") as f:
    f.write(src)
