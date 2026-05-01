import sys

with open("src/memory/mmu.rs", "r") as f:
    src = f.read()

# Let's replace the `0x04` match arm inside `write8`.
# Instead of doing it all in `write8`, I should also intercept `write16` and `write32` if I want to be safe, because some games write 32-bit to `SAD` or `DAD`.
# Wait! My `write16` and `write32` use `write8`!
# So `write8` WILL be called!
