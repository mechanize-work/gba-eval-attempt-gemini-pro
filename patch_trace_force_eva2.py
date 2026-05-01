import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('// if diff_count < 10 {', 'if diff_count < 5 { println!("Diff at {}: Em=({},{},{}) Ref=({},{},{})", i, r, g, b, ref_r, ref_g, ref_b); } \n        // if diff_count < 10 {')

with open("tests/compare.rs", "w") as f:
    f.write(src)
