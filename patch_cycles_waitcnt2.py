import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('let wait = match (waitcnt >> 24) & 0xF {', 'let wait = match (waitcnt >> 11) & 0xF {')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
