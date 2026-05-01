import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Let's check `execute_thumb_cond_branch`.
# `self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);`
# `offset` was -4.
# Trace says: PC=08000194 ... 
# PC=08000196 ... 
# Then PC=0800018E!
# Look at my log!
# Trace: PC=08000194 R0=0356DFD4 R1=0003FEE0 R2=00000000 R3=00000000 SP=03007F00 LR=08000147 Z=false (THUMB)
# Trace: PC=08000196 R0=0356DFD4 R1=0003FEDC R2=00000000 R3=00000000 SP=03007F00 LR=08000147 Z=false (THUMB)
# Trace: PC=0800018E R0=0356DFD4 R1=0003FEDC R2=00000000 R3=00000000 SP=03007F00 LR=08000147 Z=false (THUMB)
# 
# Wait!
# If it jumped from 194, the next trace would be 18E? No!
# 194 is `BNE -4`.
# If `Z=false`, it jumps!
# `194 + (-8) = 18C`??? No! `0x194` is the instruction address. `PC+4 = 0x198`.
# `0x198 + (-8) = 0x190`!
# BUT the trace says `0x196` executed!
# Why did `0x196` execute?
# The instruction AT 0x194 is `0xd1fc` (`BNE -4`).
# If `0x196` executed, that means `0x194` DID NOT JUMP!
# BUT `Z=false`, and `BNE` (NE=1) jumps when `Z=false`!
# So `0x194` DID jump! But to `0x196`? No, if it jumps, it sets `pipeline_empty=true`.
# Then `fill_pipeline()` reads `0x196`?
# NO! It should read the target!
# What if the target was `0x196`???
# Target = `self.regs[15] + (offset << 1)`.
# `offset` was -4. `offset << 1` was -8.
# What was `self.regs[15]`?
# If `self.regs[15]` was `0x19E`, then `0x19E - 8 = 0x196`!!!
# Why would `self.regs[15]` be `0x19E`?
# In `execute_thumb_cond_branch`:
# `self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);`
# `self.regs[15]` when entering `execute_thumb_cond_branch` was `0x198`.
# Then we ADDED 2! So it became `0x19A`.
# `0x19A - 8 = 0x192`!
# Wait, if it became `0x192`, then `fill_pipeline` sets `pip0=192, pip1=194, regs[15]=196`.
# Next trace prints `regs[15]-2 = 194`!
# Trace: PC=08000194!
# Wait! `Trace: PC=08000194 R1=FEA95280 ...`
# That was BEFORE!
