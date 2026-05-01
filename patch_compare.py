import sys

with open("tests/compare.rs", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "if i == 59 { println" in line:
        continue
    if "Since we didn't write to the real framebuffer" in line:
        new_lines.append("        println!(\"Frame 60 done: PC={:08X}\", gba_mut().cpu.regs[15]);\n")
    new_lines.append(line)

with open("tests/compare.rs", "w") as f:
    f.writelines(new_lines)
