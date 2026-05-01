import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if diff_count < 100 {', 'if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
