import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let mut cycle_count = 0;', 'let mut _cycle_count = 0;')
src = src.replace('cycle_count += 1;', '_cycle_count += 1;')

with open("tests/compare.rs", "w") as f:
    f.write(src)
