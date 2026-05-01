import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

new_src = src.replace("""        self.cpu.step(&mut self.mmu);
        // Assuming 1 instruction = 1 cycle for now, very inaccurate.
        self.cycles += 1;""", """        self.cpu.step(&mut self.mmu);
        // Assuming 1 instruction = 1 cycle for now, very inaccurate.
        self.cycles += 4;""")

with open("src/sys/gba.rs", "w") as f:
    f.write(new_src)
