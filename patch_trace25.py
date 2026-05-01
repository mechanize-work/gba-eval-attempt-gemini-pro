import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('let pc = gba_mut().cpu.regs[15];\n                if pc == 0x08', 'let pc = gba_mut().cpu.regs[15];\n                if gba_mut().mmu.ppu.bg2cnt != 0 { println!("BG2CNT BECOME NONZERO: {:04X}", gba_mut().mmu.ppu.bg2cnt); }\n                if pc == 0x08')

with open("tests/compare.rs", "w") as f:
    f.write(src)
