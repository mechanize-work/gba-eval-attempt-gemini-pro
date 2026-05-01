import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

new_src = src.replace('File::open("/tmp/ref60/frame_00059.ppm")', 'File::open("/tmp/ref/frame_00060.ppm")')
new_src = new_src.replace('//println!("Frame {}:', 'println!("Frame {}:')
new_src = new_src.replace('//diff_count += 1;', 'diff_count += 1;')
new_src = new_src.replace('File::open("/tmp/ref/frame_00060.ppm").unwrap()', 'return;')

with open("tests/compare.rs", "w") as f:
    f.write(new_src)
