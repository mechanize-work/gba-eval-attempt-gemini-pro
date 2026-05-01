import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

new_src = src.replace("bios: vec![0; 16 * 1024],", "bios: include_bytes!(\"../../spec/gba_bios_stub.bin\").to_vec(),")

with open("src/memory/mmu.rs", "w") as f:
    f.write(new_src)
