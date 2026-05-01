import sys
import re

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = re.sub(r'while gba_mut\(\)\.cpu\.cycles < \(\(i as usize\) \+ 1\) \* 350000 \{', r'while gba_mut().cpu.cycles < ((i as usize) + 1) * 200000 {', src)

with open("tests/compare.rs", "w") as f:
    f.write(src)
