import sys

with open("src/lib.rs", "r") as f:
    src = f.read()

new_src = src.replace("""pub extern "C" fn emu_load_rom(len: i32) -> i32 {
    unsafe {
        gba_mut().mmu.rom = vec![0; 32 * 1024 * 1024];
        gba_mut().mmu.rom[..len as usize].copy_from_slice(&ROM_BUFFER[..len as usize]);
    }
    emu_reset();
    1
}""", """pub extern "C" fn emu_load_rom(len: i32) -> i32 {
    unsafe {
        gba_mut().mmu.rom = vec![0; 32 * 1024 * 1024];
        let ptr = emu_rom_buffer();
        let buf = std::slice::from_raw_parts(ptr, len as usize);
        gba_mut().mmu.rom[..len as usize].copy_from_slice(buf);
    }
    emu_reset();
    1
}""")

with open("src/lib.rs", "w") as f:
    f.write(new_src)
