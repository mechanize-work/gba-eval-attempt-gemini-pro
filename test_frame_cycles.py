import subprocess
import re

def test_speed(frame_cycles):
    with open("src/lib.rs", "r") as f:
        src = f.read()

    src = re.sub(r'gba\.cpu\.cycles - start_cycles < \d+', f'gba.cpu.cycles - start_cycles < {frame_cycles}', src)

    with open("src/lib.rs", "w") as f:
        f.write(src)
    
    res = subprocess.run(["cargo", "test", "--test", "compare", "--", "--nocapture"], capture_output=True, text=True)
    out = res.stdout + res.stderr
    
    m = re.search(r'left: (\d+)', out)
    diff = m.group(1) if m else "ERROR"
    print(f"FRAME CYCLES={frame_cycles}: Diffs={diff}")

for cycles in [280896, 280000, 270000, 260000, 250000, 200000, 100000, 50000]:
    test_speed(cycles)

