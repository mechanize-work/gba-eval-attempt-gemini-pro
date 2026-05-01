import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Revert execute_thumb_cond_branch
src = src.replace("self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((offset << 1) as u32);", "self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);")

# Revert execute_thumb_uncond_branch
src = src.replace("self.regs[15] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 1) as u32);", "self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);")

# Revert execute_thumb_bl
src = src.replace("self.regs[14] = self.regs[15].wrapping_add(2).wrapping_add((signed_offset << 12) as u32);", "self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);")
src = src.replace("let next_pc = self.regs[15] | 1;", "let next_pc = self.regs[15].wrapping_sub(2) | 1;")

# Revert execute_thumb_pc_load
src = src.replace("let addr = (self.regs[15].wrapping_add(2) & !2).wrapping_add(imm);", "let addr = (self.regs[15] & !2).wrapping_add(imm);")

# Revert execute_thumb_load_address
src = src.replace("self.regs[rd] = (self.regs[15].wrapping_add(2) & !2).wrapping_add(imm);", "self.regs[rd] = (self.regs[15] & !2).wrapping_add(imm);")

# Revert execute_arm_branch
src = src.replace("self.regs[15] = self.regs[15].wrapping_add(4).wrapping_add((signed_offset << 2) as u32);", "self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);")
src = src.replace("self.regs[14] = self.regs[15];", "self.regs[14] = self.regs[15].wrapping_sub(4);")

# Revert execute_arm_load_store
src = src.replace("let base = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };", "let base = if rn == 15 { self.regs[15] } else { self.regs[rn] };")
src = src.replace("let base_val = if rn == 15 { self.regs[15].wrapping_add(4) } else { self.regs[rn] };", "let base_val = if rn == 15 { self.regs[15] } else { self.regs[rn] };")

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
