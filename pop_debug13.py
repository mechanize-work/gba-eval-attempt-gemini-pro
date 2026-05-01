import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Let's fix `execute_thumb_cond_branch`!
# My previous scripts attempted to fix it but `fix_branch.py` used exact string matching and failed.
# I will rewrite the function completely!
