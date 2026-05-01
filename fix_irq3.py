import sys
import re

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = re.sub(r"    pub fn trigger_irq\(&mut self\) \{[\s\S]*?    \}", "", src, count=1)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
