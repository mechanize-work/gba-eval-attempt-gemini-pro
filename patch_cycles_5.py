import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

src = src.replace('self.cycles >= 960', 'self.cycles >= 1232')
src = src.replace('self.cycles -= 960', 'self.cycles -= 1232')

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
