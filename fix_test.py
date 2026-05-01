import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

new_src = src.replace('File::open("/tmp/ref60/frame_00059.ppm")', 'File::open("/tmp/ref60/frame_00059.ppm").unwrap_or_else(|_| File::open("/tmp/ref60/frame_00059.ppm").unwrap())')
new_src = src.replace('let pc = gba_mut().cpu.regs[15];', 'let pc = gba_mut().cpu.regs[15];\n                if cycle_count > 16853000 { println!("Trace: PC={:08X} SP={:08X} R0={:08X} R1={:08X} R2={:08X}", gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }), gba_mut().cpu.regs[13], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[2]); }')

with open("tests/compare.rs", "w") as f:
    f.write(new_src)
