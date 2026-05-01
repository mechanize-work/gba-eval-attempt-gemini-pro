import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

start2 = src.find("let pc = gba_mut().cpu.regs[15];")
new_code = """
                let pc = gba_mut().cpu.regs[15];
                if pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 }) == 0x080001CC { println!("1CC EXECUTED! cycle={}", cycle_count); }
"""
src = src[:start2] + new_code + src[start2 + len("let pc = gba_mut().cpu.regs[15];"):]

with open("tests/compare.rs", "w") as f:
    f.write(src)
