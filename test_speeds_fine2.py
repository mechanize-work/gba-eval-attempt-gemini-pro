import subprocess
import re

def test_speed(cycles_vblank):
    with open("src/sys/gba.rs", "r") as f:
        src = f.read()

    src = re.sub(r'self\.cycles >= \d+', f'self.cycles >= {cycles_vblank}', src)
    src = re.sub(r'self\.cycles -= \d+', f'self.cycles -= {cycles_vblank}', src)

    with open("src/sys/gba.rs", "w") as f:
        f.write(src)
    
    res = subprocess.run(["cargo", "test", "--test", "compare", "--", "--nocapture"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    m = re.search(r'left: (\d+)', out)
    diff = m.group(1) if m else "ERROR"
    print(f"VBLANK={cycles_vblank}: Diffs={diff}")

for cycles in [1232, 1000, 800, 500, 1500, 2000, 280896]:
    test_speed(cycles)

