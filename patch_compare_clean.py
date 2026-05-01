import sys

with open("tests/compare.rs", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'println!("Trace' in line or 'println!("MEMSET' in line or 'println!("SWI called' in line or 'println!("Thumb SWI' in line or 'println!("ARM SWI' in line or 'println!("IO Write' in line:
        continue
    new_lines.append(line)

with open("tests/compare.rs", "w") as f:
    f.writelines(new_lines)
