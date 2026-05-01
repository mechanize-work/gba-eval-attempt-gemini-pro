import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('if self.cycles >= 1232 {', 'while self.cycles >= 1232 {')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
