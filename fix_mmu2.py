import sys
import re

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

# Remove duplicate DmaChannel struct
struct_pattern = r"\#\[derive\(Clone, Copy\)\]\npub struct DmaChannel \{\n    pub sad: u32,\n    pub dad: u32,\n    pub count: u16,\n    pub ctrl: u16,\n\}\n\nimpl DmaChannel \{\n    pub fn new\(\) -> Self \{\n        Self \{\n            sad: 0,\n            dad: 0,\n            count: 0,\n            ctrl: 0,\n        \}\n    \}\n\}\n"
src = src.replace(struct_pattern, "", 1) # remove first instance

# Remove duplicate pub dma: [DmaChannel; 4],
src = src.replace("pub dma: [DmaChannel; 4],\n    pub dma: [DmaChannel; 4],", "pub dma: [DmaChannel; 4],")
src = src.replace("dma: [DmaChannel::new(); 4],\n            dma: [DmaChannel::new(); 4],", "dma: [DmaChannel::new(); 4],")

# Remove duplicate trigger_dma
trigger_pattern = r"impl Mmu \{\n    pub fn trigger_dma\(&mut self, channel: usize\) \{[\s\S]*?\}\n\}\n\n\nimpl Mmu \{\n    pub fn trigger_dma\(&mut self, channel: usize\) \{[\s\S]*?\}\n\}"
src = re.sub(r"impl Mmu \{\n    pub fn trigger_dma[\s\S]*?\}\n\}\n\nimpl Mmu \{\n    pub fn trigger_dma[\s\S]*?\}\n\}", "impl Mmu {\n    pub fn trigger_dma(channel: usize) { }\n}", src) # wait, I will just write a custom script that removes the first block

with open("src/memory/mmu.rs", "w") as f:
    f.write(src)
