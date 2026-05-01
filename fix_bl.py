import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Thumb BL needs PC + 4 for the first instruction, but my step() already adds 2.
# However, my step() reads pipeline[1] then adds 2, then execute_thumb.
# So during execute_thumb, regs[15] is PC_of_instruction + 4!
# Wait, let's trace it:
# instr1 (BL prefix): PC is +4. `self.regs[14] = self.regs[15].wrapping_add(signed_offset << 12) as u32;`
# instr2 (BL suffix): PC is +4 relative to instr2.
# `let next_pc = self.regs[15].wrapping_sub(2);` -> this calculates instr2 + 2, which is the NEXT instruction! This is CORRECT for returning!
# `self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);`
# `self.regs[14] = next_pc | 1;` -> Sets LR to instr2 + 2 | 1.

# Is `offset << 12` correct? In GBA, the BL offset is 22 bits.
# Prefix: offset is shifted by 12, added to PC.
# Suffix: offset is shifted by 1, added to LR.
# The calculation in `execute_thumb_bl` seems generally correct according to docs.

# Wait, `self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);`
# But wait... for the prefix, PC is `instr1 + 4`.
# And `self.regs[15]` IS `instr1 + 4` inside `execute_thumb_bl`!
# So `self.regs[15].wrapping_add` is correct.

# What about the unconditional branch?
# `self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);`
# PC is `instr + 4`. Wait... unconditional branch offset is relative to PC+4!
# So `self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);` should be correct, because self.regs[15] is ALREADY PC+4!
# Wait, my previous fix added 2:
# `self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 1) as u32);` -> THIS WAS WRONG! It made it PC+6!
# Oh... I see. During `execute_thumb`, `self.regs[15]` is indeed `instruction + 4` because `step()` reads `pipeline[1]` (which is `instruction + 2`), then adds 2, making `self.regs[15]` equal to `instruction + 4`.
