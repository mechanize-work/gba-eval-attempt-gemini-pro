import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'for i in 0\.\.60 \{.*?println!\("End of frame.*?\}', 'for i in 0..60 {\n            emu_run_frame();\n        }', src, flags=re.DOTALL)

with open("tests/compare.rs", "w") as f:
    f.write(src)
