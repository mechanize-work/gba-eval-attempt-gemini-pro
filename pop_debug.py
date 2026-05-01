# The trace prints:
# Trace: PC=080001A0 T=true R0=00000003 R1=00000000
# Trace: PC=080001A2 T=true R0=00000003 R1=00000000
# Trace: PC=080001A4 T=true R0=00000003 R1=00000000
# Frame 59: PC: 00000000, DISPCNT: 0080, BG2CNT: 0000, PAL0: 0000, VRAM non-zero: 0
# 
# Wait, PC=0x080001A4 is the last instruction before the crash!
# Let's check what instruction is at 0x080001A4.
