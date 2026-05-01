const ROM_MAX_SIZE: usize = 32 * 1024 * 1024;
const FRAMEBUFFER_SIZE: usize = 240 * 160;
const AUDIO_BUFFER_SIZE: usize = 4096;

struct EmuState {
    rom: Vec<u8>,
    framebuffer: Vec<u32>,
    audio_buffer: Vec<i16>,
    audio_samples: i32,
}

static mut STATE: Option<EmuState> = None;

#[no_mangle]
pub extern "C" fn emu_init() -> i32 {
    let state = EmuState {
        rom: vec![0; ROM_MAX_SIZE],
        framebuffer: vec![0; FRAMEBUFFER_SIZE],
        audio_buffer: vec![0; AUDIO_BUFFER_SIZE],
        audio_samples: 0,
    };
    unsafe {
        STATE = Some(state);
    }
    1
}

#[no_mangle]
pub extern "C" fn emu_rom_buffer() -> *mut u8 {
    unsafe {
        if let Some(state) = &mut STATE {
            state.rom.as_mut_ptr()
        } else {
            std::ptr::null_mut()
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_load_rom(len: i32) -> i32 {
    // reset logic
    emu_reset();
    1
}

#[no_mangle]
pub extern "C" fn emu_reset() -> i32 {
    1
}

#[no_mangle]
pub extern "C" fn emu_set_keys(_k: u32) {
}

#[no_mangle]
pub extern "C" fn emu_run_frame() {
    unsafe {
        if let Some(state) = &mut STATE {
            // clear framebuffer and drain audio for now
            state.framebuffer.fill(0xFF000000); // solid black?
            state.audio_samples = 0;
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_framebuffer() -> *mut u32 {
    unsafe {
        if let Some(state) = &mut STATE {
            state.framebuffer.as_mut_ptr()
        } else {
            std::ptr::null_mut()
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_audio_buffer() -> *mut i16 {
    unsafe {
        if let Some(state) = &mut STATE {
            state.audio_buffer.as_mut_ptr()
        } else {
            std::ptr::null_mut()
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_audio_samples() -> i32 {
    unsafe {
        if let Some(state) = &mut STATE {
            let samples = state.audio_samples;
            state.audio_samples = 0;
            samples
        } else {
            0
        }
    }
}

#[no_mangle]
pub extern "C" fn emu_audio_rate() -> i32 {
    44100
}
