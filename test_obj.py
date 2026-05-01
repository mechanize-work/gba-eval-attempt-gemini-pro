import sys

with open("tests/compare.rs", "r") as f:
    src = f.read()

src = src.replace('println!("Map 0xE000:', 'for obj_idx in 0..128 {\n            let oam_idx = obj_idx * 8;\n            let attr0 = (gba_mut().mmu.ppu.oam[oam_idx] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 1] as u16) << 8);\n            let attr1 = (gba_mut().mmu.ppu.oam[oam_idx + 2] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 3] as u16) << 8);\n            let attr2 = (gba_mut().mmu.ppu.oam[oam_idx + 4] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 5] as u16) << 8);\n            let y = attr0 & 0xFF;\n            let x = attr1 & 0x1FF;\n            if (attr0 & 0x0300) != 0x0200 { println!("OBJ {}: x={} y={} attr0={:04X} attr1={:04X} attr2={:04X}", obj_idx, x, y, attr0, attr1, attr2); }\n        }\n        println!("Map 0xE000:')

with open("tests/compare.rs", "w") as f:
    f.write(src)
