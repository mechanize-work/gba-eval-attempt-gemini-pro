use gba_emu::gba_mut;
use std::fs::File;
use std::io::Read;
use gba_emu::{emu_init, emu_load_rom, emu_rom_buffer, emu_run_frame, emu_framebuffer};

#[test]
fn test_compare_frame_60() {
    let rom = std::fs::read("dev-roms/anguna.gba").unwrap();
    
    unsafe {
        emu_init();
        let rom_buf = std::slice::from_raw_parts_mut(emu_rom_buffer(), 32 * 1024 * 1024);
        rom_buf[..rom.len()].copy_from_slice(&rom);
        emu_load_rom(rom.len() as i32);
        
        let mut trace_count = 0;
        let mut dummy_fb = [0u32; 240 * 160];
        
        for i in 0..60 {
            for _ in 0..70224 {
                if trace_count < 100 {
                    let pc = gba_mut().cpu.regs[15];
                    let mode = gba_mut().cpu.get_mode() as u32;
                    let thumb = gba_mut().cpu.get_t();
                    let r0 = gba_mut().cpu.regs[0];
                    let r1 = gba_mut().cpu.regs[1];
                    println!("Trace: PC={:08X} Mode={:02X} Thumb={} R0={:08X} R1={:08X}", pc, mode, thumb, r0, r1);
                    trace_count += 1;
                }
                gba_mut().step(&mut dummy_fb);
            }
            if i % 10 == 0 || i == 59 {
                let pc = gba_mut().cpu.regs[15];
                let dispcnt = gba_mut().mmu.ppu.dispcnt;
                println!("Frame {}: PC: {:08X}, DISPCNT: {:04X}", i, pc, dispcnt);
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
        for i in 0..(240 * 160) {
            let r = fb[i * 4 + 0];
            let g = fb[i * 4 + 1];
            let b = fb[i * 4 + 2];
            
            let ref_r = ref_pixels[i * 3 + 0];
            let ref_g = ref_pixels[i * 3 + 1];
            let ref_b = ref_pixels[i * 3 + 2];
            
            if r != ref_r || g != ref_g || b != ref_b {
                diff_count += 1;
            }
        }
        
        println!("Frame 1 differences: {} pixels out of 38400", diff_count);
        assert_eq!(diff_count, 0, "Frames do not match!");
    }
}
