import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

import re
src = re.sub(r'if self\.cycles >= \d+ \{', 'if self.cycles >= 1232 {', src)
src = re.sub(r'self\.cycles -= \d+', 'self.cycles -= 1232', src)

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
