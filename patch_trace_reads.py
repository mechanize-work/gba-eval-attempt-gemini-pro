import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

src = src.replace('            0x04 => {', '            0x04 => { if self.wait_states > 280896*50 { println!("IO READ {:08X}", addr); }')

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count == 0 { println!("IO 50', 'gba_mut().mmu.wait_states = i * 280896;\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)

