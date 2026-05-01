# Ah!
# Let's look at `0x130` again.
# `Trace: PC=08000130 R0=00000000 R1=00000000 R2=000000E7 R3=00000000 SP=03007F00`
# Then the next line is `0x184`.
# Why did it skip `0x132`, `0x134`, `0x136`, `0x138`?!
# Because `0x130` executed!
# What is `0x130`?
# In my print of `anguna.gba` at `0x130`:
# `['0x4822', '0x4923', '0x1a09', '0xf000', '0xf826']`
# `0x4822` is `LDR r0, [pc, #136]`.
# `execute_thumb_pc_load` uses `rd = 0`, `imm = 0x22 << 2 = 0x88`.
# `addr = 0x080001BC`.
# It reads `0x03001518`.
# So `r0` becomes `0x03001518`.
# Wait. `r0` became `0x03001518`?
# In the trace for `0x184`, `r0=00000000`!
# This means `r0` DID NOT BECOME `0x03001518`!
# Or it did, and then was overwritten?
# If `0x132`..`0x138` executed, what do they do?
# `0x132`: `0x4923` -> `LDR r1, [pc, #140]`. `r1` becomes `0x0300151C`.
# `0x134`: `0x1a09` -> `SUBS r1, r1, r0`. `r1 = 0x0300151C - 0x03001518 = 4`.
# `0x136`: `0xf000`, `0xf826` -> `BL +0x4C`. Target = `0x136 + 4 + 0x4C = 0x186`.
# Wait, if target is `0x186`, why did trace print `0x184`?!
# My fix to `execute_thumb_bl` was:
# ```rust
# self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
# ```
# `regs[15]` was `0x13A`.
# `signed_offset` was `0`.
# So `regs[14]` was `0x13A`.
# Next instruction `0x138` (suffix).
# `regs[15]` was `0x13C`.
# `offset` was `0x26`.
# `self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32)`.
# `regs[15] = 0x13A + 0x4C = 0x186`.
# So `target = 0x186`!
# `fill_pipeline()` reads `pipeline[0]` from `0x186`, `regs[15] = 0x188`.
# `pipeline[1]` from `0x188`, `regs[15] = 0x18A`.
# Then `Trace` prints `regs[15] - 2` = `0x188`!
# BUT IN MY TRACE, THE FIRST THING PRINTED WAS `08000184`!
# Why did it print `08000184` instead of `08000188`?!
# Because `0x130` was NOT `0x4822`?!
# OR my `bus.read16` returns something else?!
