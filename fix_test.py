import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

start = src.find("if pc == 0x080003B2")
end = src.find("if count_a < 10 {", start)
end = src.find("}", end) + 1

if start != -1 and end != -1:
    new_code = """
                if pc == 0x080003B2 || pc == 0x08000374 { count_a += 1; }
                if count_a > 0 && count_a < 15 {
                    println!("Trace: PC={:08X} SP={:08X} LR={:08X} R0={:08X} R4={:08X} R5={:08X}", pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 }), gba_mut().cpu.regs[13], gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[4], gba_mut().cpu.regs[5]);
                    count_a += 1;
                }
"""
    src = src[:start] + new_code + src[end:]
    with open("tests/compare.rs", "w") as f:
        f.write(src)
