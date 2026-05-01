import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

# Let's insert DMA handling logic into `write8`.
dma_logic = """
                    0x0B0 => self.dma[0].sad = (self.dma[0].sad & 0xFFFFFF00) | (val as u32),
                    0x0B1 => self.dma[0].sad = (self.dma[0].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0B2 => self.dma[0].sad = (self.dma[0].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0B3 => self.dma[0].sad = (self.dma[0].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0B4 => self.dma[0].dad = (self.dma[0].dad & 0xFFFFFF00) | (val as u32),
                    0x0B5 => self.dma[0].dad = (self.dma[0].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0B6 => self.dma[0].dad = (self.dma[0].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0B7 => self.dma[0].dad = (self.dma[0].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0B8 => self.dma[0].count = (self.dma[0].count & 0xFF00) | (val as u16),
                    0x0B9 => self.dma[0].count = (self.dma[0].count & 0x00FF) | ((val as u16) << 8),
                    0x0BA => self.dma[0].ctrl = (self.dma[0].ctrl & 0xFF00) | (val as u16),
                    0x0BB => {
                        self.dma[0].ctrl = (self.dma[0].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(0); }
                    }

                    0x0BC => self.dma[1].sad = (self.dma[1].sad & 0xFFFFFF00) | (val as u32),
                    0x0BD => self.dma[1].sad = (self.dma[1].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0BE => self.dma[1].sad = (self.dma[1].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0BF => self.dma[1].sad = (self.dma[1].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0C0 => self.dma[1].dad = (self.dma[1].dad & 0xFFFFFF00) | (val as u32),
                    0x0C1 => self.dma[1].dad = (self.dma[1].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0C2 => self.dma[1].dad = (self.dma[1].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0C3 => self.dma[1].dad = (self.dma[1].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0C4 => self.dma[1].count = (self.dma[1].count & 0xFF00) | (val as u16),
                    0x0C5 => self.dma[1].count = (self.dma[1].count & 0x00FF) | ((val as u16) << 8),
                    0x0C6 => self.dma[1].ctrl = (self.dma[1].ctrl & 0xFF00) | (val as u16),
                    0x0C7 => {
                        self.dma[1].ctrl = (self.dma[1].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(1); }
                    }

                    0x0C8 => self.dma[2].sad = (self.dma[2].sad & 0xFFFFFF00) | (val as u32),
                    0x0C9 => self.dma[2].sad = (self.dma[2].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0CA => self.dma[2].sad = (self.dma[2].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0CB => self.dma[2].sad = (self.dma[2].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0CC => self.dma[2].dad = (self.dma[2].dad & 0xFFFFFF00) | (val as u32),
                    0x0CD => self.dma[2].dad = (self.dma[2].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0CE => self.dma[2].dad = (self.dma[2].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0CF => self.dma[2].dad = (self.dma[2].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0D0 => self.dma[2].count = (self.dma[2].count & 0xFF00) | (val as u16),
                    0x0D1 => self.dma[2].count = (self.dma[2].count & 0x00FF) | ((val as u16) << 8),
                    0x0D2 => self.dma[2].ctrl = (self.dma[2].ctrl & 0xFF00) | (val as u16),
                    0x0D3 => {
                        self.dma[2].ctrl = (self.dma[2].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(2); }
                    }

                    0x0D4 => self.dma[3].sad = (self.dma[3].sad & 0xFFFFFF00) | (val as u32),
                    0x0D5 => self.dma[3].sad = (self.dma[3].sad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0D6 => self.dma[3].sad = (self.dma[3].sad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0D7 => self.dma[3].sad = (self.dma[3].sad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0D8 => self.dma[3].dad = (self.dma[3].dad & 0xFFFFFF00) | (val as u32),
                    0x0D9 => self.dma[3].dad = (self.dma[3].dad & 0xFFFF00FF) | ((val as u32) << 8),
                    0x0DA => self.dma[3].dad = (self.dma[3].dad & 0xFF00FFFF) | ((val as u32) << 16),
                    0x0DB => self.dma[3].dad = (self.dma[3].dad & 0x00FFFFFF) | ((val as u32) << 24),
                    0x0DC => self.dma[3].count = (self.dma[3].count & 0xFF00) | (val as u16),
                    0x0DD => self.dma[3].count = (self.dma[3].count & 0x00FF) | ((val as u16) << 8),
                    0x0DE => self.dma[3].ctrl = (self.dma[3].ctrl & 0xFF00) | (val as u16),
                    0x0DF => {
                        self.dma[3].ctrl = (self.dma[3].ctrl & 0x00FF) | ((val as u16) << 8);
                        if (val & 0x80) != 0 { self.trigger_dma(3); }
                    }
"""

src = src.replace("                    0x209 => self.ime = (self.ime & 0x00FF) | ((val as u16) << 8),", "                    0x209 => self.ime = (self.ime & 0x00FF) | ((val as u16) << 8),\n" + dma_logic)

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
