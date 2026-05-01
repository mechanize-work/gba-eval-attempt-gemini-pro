import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if true_pc == 0x0800013E', 'if true_pc == 0x0800013C { println!("R0 AFTER 0800013A = {:08X}", gba_mut().cpu.regs[0]); }\n                if true_pc == 0x0800013E')

with open("tests/compare.rs", "w") as f:
    f.write(src)
