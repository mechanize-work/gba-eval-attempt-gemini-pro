import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace("if trace_count < 100 {", "if trace_count < 0 {")

start = src.find("let cur_sp = gba_mut().cpu.regs[13];")

new_code = """
                let true_pc = pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 });
                if true_pc >= 0x08000300 && true_pc <= 0x080003C0 && cycle_count > 16800000 {
                    if trace_count < 500 {
                        println!("Trace: PC={:08X} R0={:08X} R1={:08X} R2={:08X} SP={:08X} LR={:08X}", true_pc, gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[2], gba_mut().cpu.regs[13], gba_mut().cpu.regs[14]);
                        trace_count += 1;
                    }
                }
"""

src = src[:start] + new_code + src[start:]

with open("tests/compare.rs", "w") as f:
    f.write(src)
