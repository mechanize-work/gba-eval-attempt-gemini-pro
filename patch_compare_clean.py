import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'for _ in 0\.\.280896 \{.*?if true \{', 'emu_run_frame();\n            if true {', src, flags=re.DOTALL)
src = re.sub(r'println!\("End of frame.*?\);\n', '', src)

with open("tests/compare.rs", "w") as f:
    f.write(src)
