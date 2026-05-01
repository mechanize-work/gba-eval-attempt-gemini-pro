import sys

with open("src/sys/gba.rs", "r") as f:
    src = f.read()

irq_trigger = """
        // IRQ logic
        if self.mmu.ime != 0 {
            if (self.mmu.ie & self.mmu.i_f) != 0 {
                self.cpu.trigger_irq();
            }
        }
"""

src = src.replace("self.cpu.step(&mut self.mmu);", irq_trigger + "\n        self.cpu.step(&mut self.mmu);")

with open("src/sys/gba.rs", "w") as f:
    f.write(src)
