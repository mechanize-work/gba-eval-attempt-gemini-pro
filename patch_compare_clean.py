import sys
import re

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = re.sub(r'        if diff_count < 5 \{ println!\("Diff.*?\n', '', src)
src = re.sub(r'        if diff_count == 0 \{ println!\(.*?\n', '', src)
src = re.sub(r'        if diff_count < 10 \{ println!\(.*?\n', '', src)
src = re.sub(r'        // if diff_count.*?\n', '', src)
src = re.sub(r'        println!\("PAL0.*?\n', '', src)
src = re.sub(r'        println!\("Palette starts.*?\n', '', src)
src = re.sub(r'        println!\("CPSR=.*?\n', '', src)
src = re.sub(r'        for i in 0\.\.512 \{ let c = \(p\[i.*?\n', '', src)
src = re.sub(r'        let p = &gba_mut\(\).*?\n', '', src)

with open("tests/compare.rs", "w") as f:
    f.write(src)
