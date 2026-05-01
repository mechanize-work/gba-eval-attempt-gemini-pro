import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('for i in 0..512 { let c = (p[i*2] as u16)', 'let p = &gba_mut().mmu.ppu.palette;\n        for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); let r=c&31; let g=(c>>5)&31; let b=(c>>10)&31; if r==2 && g==4 && b==3 { println!("Found (2,4,3) at index {}", i); } }\n        for i in 0..512 { let c = (p[i*2] as u16)')

with open("tests/compare.rs", "w") as f:
    f.write(src)
