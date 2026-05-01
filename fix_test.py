import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

new_src = src.replace('gba_mut().mmu.read16(pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 }))', '0')

with open("tests/compare.rs", "w") as f:
    f.write(new_src)
