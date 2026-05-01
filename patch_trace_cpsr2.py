import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Frame 1 differences:', 'println!("CPSR={:08X} IE={:04X} IF={:04X} IME={:04X}", gba_mut().cpu.cpsr, gba_mut().mmu.ie, gba_mut().mmu.i_f, gba_mut().mmu.ime);\n        println!("Frame 1 differences:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
