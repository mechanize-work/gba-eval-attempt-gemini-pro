import subprocess

for rom_cycles in [1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20]:
    with open("src/cpu/arm7tdmi.rs", "r") as f:
        src = f.read()

    new_cycles = f"""        let cycles = match pc >> 24 {{
            0x02 => if self.get_t() {{ 3 }} else {{ 6 }},
            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => {rom_cycles},
            0x0E => 5,
            _ => 1,
        }};
        self.cycles += cycles;

        if self.get_t() {{"""

    src = src.replace('        self.cycles += 1;\n\n        if self.get_t() {', new_cycles, 1)

    with open("src/cpu/arm7tdmi.rs", "w") as f:
        f.write(src)
    
    res = subprocess.run(["cargo", "test", "--test", "compare", "--", "--nocapture"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    # restore
    subprocess.run(["git", "checkout", "src/cpu/arm7tdmi.rs"], capture_output=True)
    
    import re
    m = re.search(r'left: (\d+)', out)
    diff = m.group(1) if m else "ERROR"
    m2 = re.search(r'EVA=(\d+)', out)
    eva = m2.group(1) if m2 else "?"
    print(f"ROM CYCLES {rom_cycles}: Diffs={diff}, EVA={eva}")
