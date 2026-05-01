import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Palette starts with', 'for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); if c == 0x0421 { println!("Found 0x0421 at index {}", i); } }\n        println!("Palette starts with')

with open("tests/compare.rs", "w") as f:
    f.write(src)
