import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('bldcnt_0', 'bldcnt')

with open("tests/compare.rs", "w") as f:
    f.write(src)
