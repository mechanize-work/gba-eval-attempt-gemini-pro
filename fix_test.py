import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

start2 = src.find("let pc = gba_mut().cpu.regs[15];")
new_code = """
                let pc = gba_mut().cpu.regs[15];
                if cycle_count > 16853040 - 200 && cycle_count < 16853040 {
                    println!("Trace: PC={:08X} R0={:08X} R1={:08X}", pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 }), gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]);
                }
"""

src = src[:start2] + new_code + src[start2 + len("let pc = gba_mut().cpu.regs[15];"):]

with open("tests/compare.rs", "w") as f:
    f.write(src)
