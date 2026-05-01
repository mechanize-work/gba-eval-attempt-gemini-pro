mod cpu;
mod memory;
mod ppu;
mod sys;

use sys::gba::Gba;

static mut GBA: *mut Gba = std::ptr::null_mut();
static mut AUDIO_BUFFER: [i16; 4096] = [0; 4096];
static mut FRAMEBUFFER: [u32; 240 * 160] = [0; 240 * 160];

fn gba_mut() -> &'static mut Gba {
    unsafe {
        if GBA.is_null() {
            let b = Box::new(Gba::new());
            GBA = Box::into_raw(b);
            // Load bios
            let bios = include_bytes!("../spec/gba_bios_stub.bin");
            (*GBA).mmu.bios[..bios.len()].copy_from_slice(bios);
        }
        &mut *GBA
    }
}

#[no_mangle]
pub extern "C" fn emu_init() -> i32 {
    gba_mut();
    1
}

#[no_mangle]
pub extern "C" fn emu_rom_buffer() -> *mut u8 {
    gba_mut().mmu.rom.as_mut_ptr()
}

#[no_mangle]
pub extern "C" fn emu_load_rom(_len: i32) -> i32 {
    emu_reset();
    1
}

#[no_mangle]
pub extern "C" fn emu_reset() -> i32 {
    gba_mut().reset();
    1
}

#[no_mangle]
pub extern "C" fn emu_set_keys(_k: u32) {
}

#[no_mangle]
pub extern "C" fn emu_run_frame() {
    let gba = gba_mut();
    // 1 frame = 280896 cycles approximately
    // since we do 4 cycles per instruction: 280896 / 4 = 70224 instructions
    unsafe {
        for _ in 0..70224 {
            gba.step(&mut FRAMEBUFFER);
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_framebuffer() -> *mut u32 {
    unsafe { std::ptr::addr_of_mut!(FRAMEBUFFER) as *mut u32 }
}

#[no_mangle]
pub extern "C" fn emu_audio_buffer() -> *mut i16 {
    unsafe { std::ptr::addr_of_mut!(AUDIO_BUFFER) as *mut i16 }
}

#[no_mangle]
pub extern "C" fn emu_audio_samples() -> i32 {
    0
}

#[no_mangle]
pub extern "C" fn emu_audio_rate() -> i32 {
    32768
}
