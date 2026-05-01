import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'for _ in 0\.\.280896 \{.*?(?=if true \{)', 'emu_run_frame();\n            ', src, flags=re.DOTALL)

with open("tests/compare.rs", "w") as f:
    f.write(src)
