import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Let's check `execute_thumb_push_pop` again.
# `0xbcf0` executes `execute_thumb_push_pop`.
# `l_bit = 1` (POP), `r_bit = 1` (PC), `r_list = 0xF0` (r4-r7).
# Wait, `0xbcf0` pushes/pops r4-r7 and PC.
# `addr` comes from `regs[13]` (SP).
# `val = bus.read32(addr);`
# `self.regs[15] = val & !1;`
# Wait, what if `val` is 0?
# Then PC becomes 0!
# Why would SP have 0 at that point?
# Let's check the trace.
