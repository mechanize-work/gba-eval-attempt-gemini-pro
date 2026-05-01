import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Wait... the ARM7TDMI manual says:
# "To allow for a larger offset, the instruction is separated into two 16-bit instructions:
# 1) H=0: LR = PC + (SignExtend(offset_11) << 12)
# 2) H=1: PC = LR + (offset_11 << 1), LR = old_PC + 2 | 1"
# My code is doing exactly this:
# if (instr & 0x0800) == 0 { // H=0
#    let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
#    self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
# } else {
#    let next_pc = self.regs[15].wrapping_sub(2);
#    self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32);
#    self.regs[14] = next_pc | 1;
# }
