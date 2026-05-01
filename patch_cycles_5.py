import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cycles >= 1232', 'self.cycles >= 800')
src = src.replace('self.cycles -= 1232', 'self.cycles -= 800')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
