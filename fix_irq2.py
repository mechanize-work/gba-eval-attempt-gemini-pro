import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

irq_code = """
    pub fn trigger_irq(&mut self) {
        if (self.cpsr & 0x80) != 0 {
            return;
        }

        let ret_addr = if self.get_t() {
            self.regs[15]
        } else {
            self.regs[15].wrapping_sub(4)
        };

        let old_cpsr = self.cpsr;
        self.set_mode(Mode::Irq);
        self.banked_spsr_irq = old_cpsr;
        self.cpsr |= 0x80; // Disable IRQs
        self.set_t(false); // Switch to ARM mode

        self.regs[14] = ret_addr;
        self.regs[15] = 0x18;
        self.reload_pipeline();
    }
"""

src = src.replace("pub fn new() -> Self {", irq_code + "\n    pub fn new() -> Self {")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
