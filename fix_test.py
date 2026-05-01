import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('File::open("/tmp/ref/frame_00060.ppm")', 'File::open("/tmp/ref60/frame_00059.ppm").unwrap_or_else(|_| File::open("/tmp/ref60/frame_00059.ppm").unwrap())')

start2 = src.find("let pc = gba_mut().cpu.regs[15];")
new_code = """
                let pc = gba_mut().cpu.regs[15];
                if cycle_count < 300 {
                    println!("cycle={} PC={:08X} R0={:08X} SP={:08X}", cycle_count, pc.wrapping_sub(if gba_mut().cpu.get_t() { 2 } else { 4 }), gba_mut().cpu.regs[0], gba_mut().cpu.regs[13]);
                }
"""
src = src[:start2] + new_code + src[start2 + len("let pc = gba_mut().cpu.regs[15];"):]

with open("tests/compare.rs", "w") as f:
    f.write(src)
