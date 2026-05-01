import subprocess
import re

def test_speed(ewram, rom_s, sram):
    src_template = f"""        let cycles = match pc >> 24 {{
            0x02 => {ewram},
            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => {rom_s},
            0x0E => {sram},
            _ => 1,
        }};
        self.cycles += cycles;

        if self.get_t() {{"""
        
    with open("src/cpu/arm7tdmi.rs", "r") as f:
        src = f.read()

    src = re.sub(r'        let cycles = match pc >> 24 \{.*?if self\.get_t\(\) \{', src_template, src, flags=re.DOTALL, count=1)

    with open("src/cpu/arm7tdmi.rs", "w") as f:
        f.write(src)
    
    res = subprocess.run(["cargo", "test", "--test", "compare", "--", "--nocapture"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    subprocess.run(["git", "checkout", "src/cpu/arm7tdmi.rs"], capture_output=True)
    
    m = re.search(r'left: (\d+)', out)
    diff = m.group(1) if m else "ERROR"
    m2 = re.search(r'EVA=(\d+)', out)
    eva = m2.group(1) if m2 else "?"
    print(f"EWRAM={ewram} ROM={rom_s} SRAM={sram}: Diffs={diff}, EVA={eva}")

for ewram in [3, 4, 6]:
    for rom_s in [1, 2, 3, 4]:
        for sram in [5, 10]:
            test_speed(ewram, rom_s, sram)

