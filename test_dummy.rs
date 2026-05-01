fn main() {
    let mut fb = [0u32; 1];
    fb[0] = 0xFFFFFFFF;
    let r = (fb[0] & 0xFF) as u8;
    let g = ((fb[0] >> 8) & 0xFF) as u8;
    let b = ((fb[0] >> 16) & 0xFF) as u8;
    println!("{},{},{}", r,g,b);
}
