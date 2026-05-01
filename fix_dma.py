import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

start = src.find("impl Mmu {\n    pub fn trigger_dma", 100)
end = src.find("impl Bus for Mmu {")
if start != -1 and end != -1:
    src = src[:start] + src[end:]

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
