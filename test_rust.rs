fn main() {
    let offset = 0x4F0;
    let mut signed_offset = offset;
    if (signed_offset & 0x400) != 0 {
        signed_offset |= !0x7FF;
    }
    println!("{:08X}", (signed_offset << 12) as u32);
}
