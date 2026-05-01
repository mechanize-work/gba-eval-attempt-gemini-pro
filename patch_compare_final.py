import sys
import re

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = re.sub(r'        for i in 0\.\.60 \{.*?let mut diff_count = 0;', '        let mut diff_count = 0;\n        for i in 0..60 {\n            emu_run_frame();\n        }', src, flags=re.DOTALL)
src = re.sub(r'        if diff_count < 5 \{ println!\("Diff.*?\n', '', src)
src = re.sub(r'        if diff_count == 0 \{ println!\(.*?\n', '', src)
src = re.sub(r'        if gba_mut\(\).*?println!\(.*?\n', '', src)
src = re.sub(r'        if count_a.*?println!\(.*?\n', '', src)
src = re.sub(r'        if \(gba_mut\(\).*?println!\(.*?\n', '', src)

with open("tests/compare.rs", "w") as f:
    f.write(src)
