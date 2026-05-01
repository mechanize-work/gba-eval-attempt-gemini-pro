import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if pc == 0x0800016C { println!("REACHED 0800016C!"); }', 'if pc == 0x0800014A { println!("REACHED 0800014A!"); }\n                if pc == 0x08000154 { println!("REACHED 08000154!"); }')

with open("tests/compare.rs", "w") as f:
    f.write(src)
