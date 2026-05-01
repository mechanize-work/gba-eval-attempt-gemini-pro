use std::fs::File;
use std::io::Read;
use gba_emu::gba_mut;
use gba_emu::{emu_init, emu_load_rom, emu_rom_buffer, emu_run_frame, emu_framebuffer};

#[test]
fn test_compare_frame_60() {
    let rom = std::fs::read("dev-roms/anguna.gba").unwrap();

    unsafe {
        emu_init();
        let rom_buf = std::slice::from_raw_parts_mut(emu_rom_buffer(), 32 * 1024 * 1024);
        rom_buf[..rom.len()].copy_from_slice(&rom);
        emu_load_rom(rom.len() as i32);

        let mut dummy_fb = [0u32; 240 * 160];
        let mut _cycle_count = 0; let mut count_a = 0;
        let mut prev_pc_region = 0;

        for i in 0..60 {
            println!("End of frame {}: PC={:08X} r1={:08X}", i, gba_mut().cpu.regs[15], gba_mut().cpu.regs[1]);
            for _ in 0..280896 {
                
                let pc = gba_mut().cpu.regs[15];
                if pc == 0x0800014A { println!("REACHED 0800014A!"); }
                if pc == 0x08000154 { println!("REACHED 08000154!"); }
                if pc == 0x08000196 && gba_mut().cpu.regs[1] == 0 { println!("R1 IS 0! Z={}", gba_mut().cpu.get_z()); }
                if pc == 0x08000196 { println!("AT 08000196 LR={:08X} R0={:08X} R1={:08X} cycles={}", gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], _cycle_count); }
                let true_pc = pc.wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 });
                if true_pc == 0x0800013C { println!("R0 AFTER 0800013A = {:08X}", gba_mut().cpu.regs[0]); }
                if true_pc == 0x0800013E { println!("R0={:08X} R1={:08X} LR={:08X} BEFORE SUBS", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], gba_mut().cpu.regs[14]); }
                if true_pc == 0x08000186 {
                }

                let region = pc >> 24;

                if pc == 0x00000010 {
                    // We just jumped to SWI vector
                    let lr = gba_mut().cpu.regs[14];
                    let t = gba_mut().cpu.spsr & 0x20 != 0;
                    if t {
                        // It was a thumb SWI
                        let swi_addr = lr.wrapping_sub(2);
                        let offset = (swi_addr & 0x1FFFFFF) as usize;
                        let swi_instr = if swi_addr >> 24 == 8 {
                            gba_mut().mmu.rom[offset] as u16 | ((gba_mut().mmu.rom[offset+1] as u16) << 8)
                        } else {
                            0
                        };
                    } else {
                        // It was an ARM SWI
                        let swi_addr = lr.wrapping_sub(4);
                        let offset = (swi_addr & 0x1FFFFFF) as usize;
                        let swi_instr = if swi_addr >> 24 == 8 {
                            gba_mut().mmu.rom[offset] as u32 | ((gba_mut().mmu.rom[offset+1] as u32) << 8) | ((gba_mut().mmu.rom[offset+2] as u32) << 16) | ((gba_mut().mmu.rom[offset+3] as u32) << 24)
                        } else {
                            0
                        };
                    }
                }
                
                if region != prev_pc_region {
                    let mode = gba_mut().cpu.get_mode() as u32;
                    let thumb = gba_mut().cpu.get_t();
                    
                    prev_pc_region = region;
                }
                
                
                let true_pc = gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }); count_a += 1;
                if gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }) == 0x080003B6 || gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }) == 0x080003B8 || gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }) == 0x080003BA || gba_mut().cpu.regs[15].wrapping_sub(if gba_mut().cpu.get_t() { 4 } else { 8 }) == 0x080003BC {
                    count_a += 1;
                }

gba_mut().step(&mut dummy_fb); _cycle_count += 1;
            }
            if true {
                let pc = gba_mut().cpu.regs[15];
                if pc == 0x0800014A { println!("REACHED 0800014A!"); }
                if pc == 0x08000154 { println!("REACHED 08000154!"); }
                if pc == 0x08000196 && gba_mut().cpu.regs[1] == 0 { println!("R1 IS 0! Z={}", gba_mut().cpu.get_z()); }
                if pc == 0x08000196 { println!("AT 08000196 LR={:08X} R0={:08X} R1={:08X} cycles={}", gba_mut().cpu.regs[14], gba_mut().cpu.regs[0], gba_mut().cpu.regs[1], _cycle_count); }
                let dispcnt = gba_mut().mmu.ppu.dispcnt;
                let bg2cnt = gba_mut().mmu.ppu.bg2cnt;
                let pal0 = gba_mut().mmu.ppu.palette[0];
                let pal1 = gba_mut().mmu.ppu.palette[1];
                let mut nonzero_vram = 0;
                for b in gba_mut().mmu.ppu.vram.iter() { if *b != 0 { nonzero_vram += 1; } }
            }
        }
        
        for fb_frame in 1..=60 { println!("Frame {} ended at PC={:08X}", fb_frame, gba_mut().cpu.regs[15]); }
        // Since we didn't write to the real framebuffer, let's copy dummy_fb to test
        let mut fb = [0u8; 240 * 160 * 4];
        for i in 0..240*160 {
            fb[i*4] = (dummy_fb[i] & 0xFF) as u8;
            fb[i*4+1] = ((dummy_fb[i] >> 8) & 0xFF) as u8;
            fb[i*4+2] = ((dummy_fb[i] >> 16) & 0xFF) as u8;
        }
        
        let mut ref_file = File::open("/tmp/ref60/frame_00059.ppm").unwrap();
        let mut ref_data = Vec::new();
        ref_file.read_to_end(&mut ref_data).unwrap();
        
        // Find the start of the pixel data in the PPM (after the 3rd newline)
        let mut newlines = 0;
        let mut data_start = 0;
        for (i, &b) in ref_data.iter().enumerate() {
            if b == b'\n' {
                newlines += 1;
                if newlines == 3 {
                    data_start = i + 1;
                    break;
                }
            }
        }
        
        let ref_pixels = &ref_data[data_start..];
        
        let mut diff_count = 0;
        let mut printed = 0;
        for i in 0..(240 * 160) {
            let r = fb[i * 4 + 0];
            let g = fb[i * 4 + 1];
            let b = fb[i * 4 + 2];
            
            let ref_r = ref_pixels[i * 3 + 0];
            let ref_g = ref_pixels[i * 3 + 1];
            let ref_b = ref_pixels[i * 3 + 2];
            
            if r != ref_r || g != ref_g || b != ref_b {
                if printed < 10 {
                    if diff_count == 0 { println!("PAL0: {:02X}{:02X}", gba_mut().mmu.ppu.palette[1], gba_mut().mmu.ppu.palette[0]); }
        if diff_count < 5 { println!("Diff at {}: Em=({},{},{}) Ref=({},{},{})", i, r, g, b, ref_r, ref_g, ref_b); } 
        if diff_count < 5 { println!("Diff at {}: target1={} target2={} effect={} eva={} evb={}", i, gba_mut().mmu.ppu.bldcnt & 0x3F, (gba_mut().mmu.ppu.bldcnt >> 8) & 0x3F, (gba_mut().mmu.ppu.bldcnt >> 6) & 3, gba_mut().mmu.ppu.bldalpha & 0x1F, (gba_mut().mmu.ppu.bldalpha >> 8) & 0x1F); }
        if diff_count == 0 { println!("IE={:04X} IF={:04X} DISPSTAT={:04X}", gba_mut().mmu.ie, gba_mut().mmu.i_f, gba_mut().mmu.ppu.dispstat); }
        if gba_mut().cpu.regs[15] == 0x18 { println!("IRQ FIRED!"); }
        if diff_count == 0 { println!("BLDCNT={:04X} BLDALPHA={:04X}", gba_mut().mmu.ppu.bldcnt, gba_mut().mmu.ppu.bldalpha); }
        if diff_count == 0 { println!("Frame {} EVA={}", i, gba_mut().mmu.ppu.bldalpha & 0x1F); }
        // if diff_count < 10 { IO 50={:04X} 52={:04X} 54={:04X}", i, gba_mut().mmu.ppu.bldcnt, gba_mut().mmu.ppu.bldalpha, gba_mut().mmu.ppu.bldy); } 
        // if diff_count == 0 { 52={:04X} 54={:04X}", gba_mut().mmu.ppu.bldcnt, gba_mut().mmu.ppu.bldalpha, gba_mut().mmu.ppu.bldy); } 
        if diff_count == 0 { println!("DMA3: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[3].sad, gba_mut().mmu.dma[3].dad, gba_mut().mmu.dma[3].count, gba_mut().mmu.dma[3].ctrl); }
        // println!("DMA0: {:08X} {:08X} {:04X} {:04X} DMA1: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[0].sad, gba_mut().mmu.dma[0].dad, gba_mut().mmu.dma[0].count, gba_mut().mmu.dma[0].ctrl, gba_mut().mmu.dma[1].sad, gba_mut().mmu.dma[1].dad, gba_mut().mmu.dma[1].count, gba_mut().mmu.dma[1].ctrl); }
        // println!("DMA3: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[3].sad, gba_mut().mmu.dma[3].dad, gba_mut().mmu.dma[3].count, gba_mut().mmu.dma[3].ctrl); }
        // println!("DMA0: {:08X} {:08X} {:04X} {:04X}", gba_mut().mmu.dma[0].sad, gba_mut().mmu.dma[0].dad, gba_mut().mmu.dma[0].count, gba_mut().mmu.dma[0].ctrl); }
        if diff_count < 10 { println!("VBLANKS: {}", count_a); }
        if gba_mut().mmu.ppu.bldalpha & 0x1F != 0 { println!("EVA = {}", gba_mut().mmu.ppu.bldalpha & 0x1F); }
        if gba_mut().cpu.regs[15] == 0x08012A46 && count_a % 10000 == 0 { println!("Stuck at 08012A46! R0={:08X} R1={:08X}", gba_mut().cpu.regs[0], gba_mut().cpu.regs[1]); }
        if count_a % 100000 == 0 { println!("IE={:04X} IF={:04X}", gba_mut().mmu.ie, gba_mut().mmu.i_f); }
        if (gba_mut().mmu.ppu.bldalpha & 0x1F) != 0 { println!("EVA={} at PC={:08X}", gba_mut().mmu.ppu.bldalpha & 0x1F, gba_mut().cpu.regs[15]); }
        if count_a == 1 { println!("WAITCNT={:04X}", gba_mut().mmu.waitcnt); }
        if i == 59 { gba_mut().mmu.ppu.bldalpha = 0x0F0D; }
        if count_a == 1 { println!("WAITCNT={:04X}", gba_mut().mmu.waitcnt); }
        if count_a % 100000 == 0 { println!("Frame {} PC={:08X} count_a={}", i, gba_mut().cpu.regs[15], count_a); }
        if _cycle_count % 1000000 == 0 { println!("PC={:08X} count={}", gba_mut().cpu.regs[15], _cycle_count); }
        if count_a == 1 { println!("CPSR I-BIT={}", (gba_mut().cpu.cpsr >> 7) & 1); }
        if count_a % 10000 == 0 { println!("PC={:08X} IME={}", gba_mut().cpu.regs[15], gba_mut().mmu.ime); }
        if (gba_mut().mmu.ppu.bldalpha & 0x1F) > 0 { println!("EVA={} at frame {}", gba_mut().mmu.ppu.bldalpha & 0x1F, i); }
        // if diff_count == 0 { println!("IO 50={:04X} 52={:04X} 54={:04X}", (gba_mut().mmu.ppu.bldcnt as u16), gba_mut().mmu.ppu.bldalpha, gba_mut().mmu.ppu.bldy); } 
        println!("Diff at {}: Em=({},{},{}) Ref=({},{},{})", i, r, g, b, ref_r, ref_g, ref_b);
                    printed += 1;
                }
                diff_count += 1;
            }
        }
        
        let mut nonzero = 0; for i in 0..96*1024 { if gba_mut().mmu.ppu.vram[i] != 0 { nonzero += 1; } } println!("VRAM Non-zero bytes: {}", nonzero);
        let map_val = (gba_mut().mmu.ppu.vram[0xE000] as u16) | ((gba_mut().mmu.ppu.vram[0xE001] as u16) << 8); let p = &gba_mut().mmu.ppu.palette;
        let p = &gba_mut().mmu.ppu.palette;
        for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); let r=c&31; let g=(c>>5)&31; let b=(c>>10)&31; if r==2 && g==4 && b==3 { println!("Found (2,4,3) at index {}", i); } }
        for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); if c == 0x0421 { println!("Found 0x0421 at index {}", i); } }
        println!("VRAM 0: {:02X} {:02X}", gba_mut().mmu.ppu.vram[0], gba_mut().mmu.ppu.vram[1]);
        for obj_idx in 0..128 {
            let oam_idx = obj_idx * 8;
            let attr0 = (gba_mut().mmu.ppu.oam[oam_idx] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 1] as u16) << 8);
            let attr1 = (gba_mut().mmu.ppu.oam[oam_idx + 2] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 3] as u16) << 8);
            let attr2 = (gba_mut().mmu.ppu.oam[oam_idx + 4] as u16) | ((gba_mut().mmu.ppu.oam[oam_idx + 5] as u16) << 8);
            let y = attr0 & 0xFF;
            let x = attr1 & 0x1FF;
            if (attr0 & 0x0300) != 0x0200 { println!("OBJ {}: x={} y={} attr0={:04X} attr1={:04X} attr2={:04X}", obj_idx, x, y, attr0, attr1, attr2); }
        }
        println!("Map 0xE000: {:04X}", map_val);
        println!("BG2HOFS: {:04X}, BG2VOFS: {:04X}", gba_mut().mmu.ppu.bg2hofs, gba_mut().mmu.ppu.bg2vofs);
        println!("PAL0: {:02X}{:02X}, DISPCNT: {:04X}, BG0CNT: {:04X}", gba_mut().mmu.ppu.palette[1], gba_mut().mmu.ppu.palette[0], gba_mut().mmu.ppu.dispcnt, gba_mut().mmu.ppu.bg0cnt);
        let p = &gba_mut().mmu.ppu.palette;
        let p = &gba_mut().mmu.ppu.palette;
        let p = &gba_mut().mmu.ppu.palette;
        for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); let r=c&31; let g=(c>>5)&31; let b=(c>>10)&31; if r==2 && g==4 && b==3 { println!("Found (2,4,3) at index {}", i); } }
        for i in 0..512 { let c = (p[i*2] as u16) | ((p[i*2+1] as u16) << 8); if c == 0x0421 { println!("Found 0x0421 at index {}", i); } }
        println!("Palette starts with: {:02X}{:02X} {:02X}{:02X} {:02X}{:02X} {:02X}{:02X}", p[1], p[0], p[3], p[2], p[5], p[4], p[7], p[6]);
        println!("CPSR={:08X} IE={:04X} IF={:04X} IME={:04X}", gba_mut().cpu.cpsr, gba_mut().mmu.ie, gba_mut().mmu.i_f, gba_mut().mmu.ime);
        println!("Frame 1 differences: {} pixels out of 38400", diff_count);
        assert_eq!(diff_count, 0, "Frames do not match!");
    }
}
