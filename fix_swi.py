import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

new_src = src.replace("fn handle_hle_swi(&mut self, swi_num: u32, bus: &mut dyn Bus) -> bool {", "fn handle_hle_swi(&mut self, swi_num: u32, bus: &mut dyn Bus) -> bool {\n        println!(\"SWI called {:02X}\", swi_num);")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
