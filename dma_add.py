import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

dma_struct = """
#[derive(Clone, Copy)]
pub struct DmaChannel {
    pub sad: u32,
    pub dad: u32,
    pub count: u16,
    pub ctrl: u16,
}

impl DmaChannel {
    pub fn new() -> Self {
        Self {
            sad: 0,
            dad: 0,
            count: 0,
            ctrl: 0,
        }
    }
}
"""

src = src.replace("pub struct Mmu {", dma_struct + "\npub struct Mmu {")
src = src.replace("pub ppu: Ppu,", "pub ppu: Ppu,\n    pub dma: [DmaChannel; 4],")
src = src.replace("ppu: Ppu::new(),", "ppu: Ppu::new(),\n            dma: [DmaChannel::new(); 4],")

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
