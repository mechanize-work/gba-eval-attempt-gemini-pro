# Ah!
# Let's check the trace!
# Trace: PC=08000192 T=true Z=true R0=02000000 R1=00040000
# Trace: PC=08000194 T=true Z=true R0=02000004 R1=00040000
# Trace: PC=08000196 T=true Z=false R0=02000004 R1=0003FFFC
# Look at PC=08000196!
# If `0x194` (BNE) branched to `0x190`, the trace should print `PC=08000190`!
# Because `fill_pipeline()` loads `0x190` into `pipeline[0]`.
# Then `regs[15]` becomes `0x194`.
# Then `Trace: PC={:08X}` prints `regs[15] - 2`, which is `0x192`!
# Wait! If it branched to `0x190`, the trace WOULD print `PC=08000192`!
# BUT IT PRINTED `PC=08000196`!
# So it DID NOT BRANCH!
# Why did it not branch?
# Because AT `0x194`, `Z=true` in the trace!
# Trace: PC=08000194 T=true Z=true R0=02000004 R1=00040000
# At 0x194, Z is true!
# So `!Z` is false!
# So `execute_thumb_cond_branch` does NOT branch!
# WHY WAS Z=true???
# The instruction AT `0x192` is `0x3904` (SUBS r1, #4).
# `Trace: PC=08000194` means `0x192` just finished executing!
# Wait, NO!
# My trace prints BEFORE `step()`!
# `let pc = gba_mut().cpu.regs[15]; println!("Trace: PC={:08X}", pc - 2);`
# `gba_mut().step(&mut dummy_fb);`
# If `pc - 2` is `0x194`, then `0x194` is ABOUT TO EXECUTE!
# The instruction BEFORE `0x194` is `0x192` (SUBS r1, #4).
# In the trace for `PC=08000194`, R1 is ALREADY `00040000`. Wait!
# Trace for 0x192: `PC=08000192 ... R1=00040000`.
# Trace for 0x194: `PC=08000194 ... R1=00040000`.
# So `SUBS r1, #4` at 0x192 DID NOT CHANGE R1???
# Why did `0x3904` not change R1?
