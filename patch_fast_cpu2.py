import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'self\.cycles \+= self\.get_memory_cycles_32.*?;\n', '', src)
src = re.sub(r'self\.cycles \+= \(count as usize\) \* \(self\.get_memory_cycles_32.*?;\n', '', src)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
