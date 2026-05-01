import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

# GBA colors are 5 bits. 0-31. When rendering to 8-bit, 31 becomes 255.
# My current scaling: let r = (c & 0x1F) << 3;
# A better scaling is (color << 3) | (color >> 2). Or for now just let's see if this matches reference better.
# Mesen/VBA uses specific color curve or just standard. The oracle might just use (c & 0x1F) << 3 or standard mapping. Wait, my code does `let r = (c & 0x1F) << 3;`
# Wait, let's look at the oracle's output: (16,33,24).
# 16 >> 3 = 2. 33 >> 3 = 4. 24 >> 3 = 3.
# Let's see if my palette has color (2,4,3) but I output (0,0,0)?
