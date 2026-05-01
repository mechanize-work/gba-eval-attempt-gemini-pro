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
        let mut cycle_count = 0;
        let mut cycle_count = 0;
        let mut prev_pc_region = 0;

        for i in 0..60 {
            for _ in 0..280896 {
                let pc = gba_mut().cpu.regs[15];
                let region = pc >> 24;

                // Track SWI
                if pc == 0x00000008 {
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
                        println!("Thumb SWI called: {:02X}", swi_instr & 0xFF);
                    } else {
                        // It was an ARM SWI
                        let swi_addr = lr.wrapping_sub(4);
                        let offset = (swi_addr & 0x1FFFFFF) as usize;
                        let swi_instr = if swi_addr >> 24 == 8 {
                            gba_mut().mmu.rom[offset] as u32 | ((gba_mut().mmu.rom[offset+1] as u32) << 8) | ((gba_mut().mmu.rom[offset+2] as u32) << 16) | ((gba_mut().mmu.rom[offset+3] as u32) << 24)
                        } else {
                            0
                        };
                        println!("ARM SWI called: {:06X}", swi_instr & 0xFFFFFF);
                    }
                }
                
                if region != prev_pc_region {
                    let mode = gba_mut().cpu.get_mode() as u32;
                    let thumb = gba_mut().cpu.get_t();
                    
                    prev_pc_region = region;
                }
                
                if cycle_count < 300 {
                    let pc = gba_mut().cpu.regs[15];
                    let r0 = gba_mut().cpu.regs[0];
                    let r1 = gba_mut().cpu.regs[1];
                    let r2 = gba_mut().cpu.regs[2];
                    let r3 = gba_mut().cpu.regs[3];
                    let t = gba_mut().cpu.get_t();
                    println!("Trace: PC={:08X} R0={:08X} R1={:08X} R2={:08X} R3={:08X}", pc.wrapping_sub(2), r0, r1, r2, r3);
                    
                }
                gba_mut().step(&mut dummy_fb); cycle_count += 1;
            }
            if true {
                let pc = gba_mut().cpu.regs[15];
                let dispcnt = gba_mut().mmu.ppu.dispcnt;
                let bg2cnt = gba_mut().mmu.ppu.bg2cnt;
                let pal0 = gba_mut().mmu.ppu.palette[0];
                let pal1 = gba_mut().mmu.ppu.palette[1];
                let mut nonzero_vram = 0;
                for b in gba_mut().mmu.ppu.vram.iter() { if *b != 0 { nonzero_vram += 1; } }
                if i == 59 { println!("Frame {}: PC: {:08X}, DISPCNT: {:04X}, BG2CNT: {:04X}, PAL0: {:02X}{:02X}, VRAM non-zero: {}", i, pc, dispcnt, bg2cnt, pal1, pal0, nonzero_vram); }
            }
        }
        
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
                    println!("Diff at {}: Em=({},{},{}) Ref=({},{},{})", i, r, g, b, ref_r, ref_g, ref_b);
                    printed += 1;
                }
                diff_count += 1;
            }
        }
        
        println!("Frame 1 differences: {} pixels out of 38400", diff_count);
        assert_eq!(diff_count, 0, "Frames do not match!");
    }
}
