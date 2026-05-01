# Ah!
# Let's check the trace!
# Trace: PC=0800019E T=true Z=false R0=00000000 R1=00000000 R2=00000003 R3=FFFFFFFD SP=03007F00 LR=08000133
# Instruction at 0x19A: `0x2003` -> MOV r0, #3. (wait, trace skips 0x19A and 0x19C)
# Wait! At 0x19E, R0 is 0! It SHOULD BE 3!
# Why did it skip 0x19A and 0x19C?
# Ah! The previous instruction was at 0x198!
# `0x198` is `1aa3` -> `SUBS r3, r4, r2`.
# PC+4 = 0x19C. Wait, no. Trace says `PC=08000198`.
# So instruction is at `0x194`.
# Let's review the code starting at 0x18e.
