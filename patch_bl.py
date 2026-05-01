import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

src = src.replace('println!("BL Target: {:08X}", target);', 'println!("BL Target: {:08X} from {:08X}", target, self.regs[15]);')

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
