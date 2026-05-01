import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('            0x04 => { // IntrWait\n                let wait_flags = self.regs[1];',
                  '            0x04 => { // IntrWait\n                println!("SWI 4 CALLED at cycle {}", self.cycles);\n                let wait_flags = self.regs[1];')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
