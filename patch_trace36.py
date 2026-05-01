import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('if diff_count == 0 { println!("IO 50', 'if diff_count < 10 { println!("VBLANKS: {}", count_a); }\n        // if diff_count == 0 { println!("IO 50')

with open("tests/compare.rs", "w") as f:
    f.write(src)
