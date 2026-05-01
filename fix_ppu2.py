import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

# I am rendering black (0,0,0), so my PPU isn't drawing anything there.
# Let's check my sprite logic.
