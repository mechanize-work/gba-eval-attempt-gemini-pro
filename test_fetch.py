import struct
data=open('dev-roms/anguna.gba', 'rb').read()

pc = 0x08000000
for _ in range(10):
    val = struct.unpack('<I', data[pc-0x08000000:pc-0x08000000+4])[0]
    print(f"PC: {hex(pc)} => {hex(val)}")
    # compute next PC
    offset = val & 0xFFFFFF
    if offset & 0x800000:
        offset |= ~0xFFFFFF
    # B instruction
    if (val >> 24) & 0xF == 0xA:
        pc = pc + 8 + (offset << 2)
    else:
        pc += 4

