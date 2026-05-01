import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    pub fn check_cond(&self, cond: u32) -> bool {
        let n = self.get_n();
        let z = self.get_z();
        let c = self.get_c();
        let v = self.get_v();

        match cond {
            0x0 => z,                   // EQ
            0x1 => !z,                  // NE
            0x2 => c,                   // CS
            0x3 => !c,                  // CC
            0x4 => n,                   // MI
            0x5 => !n,                  // PL
            0x6 => v,                   // VS
            0x7 => !v,                  // VC
            0x8 => c && !z,             // HI
            0x9 => !c || z,             // LS
            0xA => n == v,              // GE
            0xB => n != v,              // LT
            0xC => !z && (n == v),      // GT
            0xD => z || (n != v),       // LE""", """    pub fn check_cond(&self, cond: u32) -> bool {
        let n = self.get_n();
        let z = self.get_z();
        let c = self.get_c();
        let v = self.get_v();

        match cond {
            0x0 => z,                   // EQ
            0x1 => !z,                  // NE
            0x2 => c,                   // CS
            0x3 => !c,                  // CC
            0x4 => n,                   // MI
            0x5 => !n,                  // PL
            0x6 => v,                   // VS
            0x7 => !v,                  // VC
            0x8 => c && !z,             // HI
            0x9 => !c || z,             // LS
            0xA => n == v,              // GE
            0xB => n != v,              // LT
            0xC => !z && (n == v),      // GT
            0xD => z || (n != v),       // LE""")

print("Replaced" if new_src != src else "Unchanged")
