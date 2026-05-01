import re

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

# remove duplicate block in write8
pattern = r"( {20}0x0B0 => self\.dma\[0\]\.sad[\s\S]*?if \(val & 0x80\) != 0 \{ self\.trigger_dma\(3\); \}\n {20}\}\n)"

matches = list(re.finditer(pattern, src))
if len(matches) == 2:
    print("Found 2 blocks, removing second one")
    # Replace the second occurrence with empty string
    new_src = src[:matches[1].start()] + src[matches[1].end():]
    with open("src/memory/mmu.rs", "w") as f:
        f.write(new_src)
elif len(matches) > 2:
    print(f"Found {len(matches)} blocks!")
else:
    print(f"Found {len(matches)} blocks, could not fix")
