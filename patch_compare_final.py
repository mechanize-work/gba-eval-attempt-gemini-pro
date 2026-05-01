import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

import re
# Replace the inner loop with emu_run_frame()
src = re.sub(r'for _ in 0\.\.280896 \{.*?\}', 'emu_run_frame();', src, flags=re.DOTALL)

with open("tests/compare.rs", "w") as f:
    f.write(src)
