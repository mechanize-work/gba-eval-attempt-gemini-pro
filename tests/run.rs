use std::fs::File;
use std::io::Write;
use gba_emu::{emu_init, emu_load_rom, emu_rom_buffer, emu_run_frame, emu_framebuffer};

#[test]
fn test_emu_run() {
    let rom = std::fs::read("dev-roms/anguna.gba").unwrap();
    
    unsafe {
        emu_init();
        let rom_buf = std::slice::from_raw_parts_mut(emu_rom_buffer(), 32 * 1024 * 1024);
        rom_buf[..rom.len()].copy_from_slice(&rom);
        emu_load_rom(rom.len() as i32);
        
        println!("Running 1 frame...");
        emu_run_frame();
        
        let fb_ptr = emu_framebuffer();
        let fb = std::slice::from_raw_parts(fb_ptr as *const u8, 240 * 160 * 4);
        
        // Write as PPM
        let mut file = File::create("/tmp/my_frame.ppm").unwrap();
        write!(file, "P6\n240 160\n255\n").unwrap();
        
        for i in 0..(240 * 160) {
            let r = fb[i * 4 + 0];
            let g = fb[i * 4 + 1];
            let b = fb[i * 4 + 2];
            file.write_all(&[r, g, b]).unwrap();
        }
    }
}
