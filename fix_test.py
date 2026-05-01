import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

start2 = src.find("let pc = gba_mut().cpu.regs[15];")
new_code = """
                let pc = gba_mut().cpu.regs[15];
                let true_pc = pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 });
                if true_pc >= 0x0800013A && true_pc <= 0x08000140 {
                    println!("Trace: PC={:08X} R0={:08X} R1={:08X} R2={:08X}", true_pc, gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[2]);
                }
"""
src = src[:start2] + new_code + src[start2 + len("let pc = gba_mut().cpu.regs[15];"):]

with open("tests/compare.rs", "w") as f:
    f.write(src)
