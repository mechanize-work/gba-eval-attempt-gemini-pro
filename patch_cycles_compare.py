import sys
import re

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = re.sub(r'for _ in 0\.\.280896 \{', r'while gba_mut().cpu.cycles < ((i as usize) + 1) * 280896 {', src)

with open("tests/compare.rs", "w") as f:
    f.write(src)
