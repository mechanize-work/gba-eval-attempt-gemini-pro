import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("BG2CNT BECOME', '//')

with open("tests/compare.rs", "w") as f:
    f.write(src)
