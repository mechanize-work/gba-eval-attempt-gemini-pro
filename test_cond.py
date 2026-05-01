import sys
with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()
if "fn execute_thumb_cond_branch" in src:
    print("Found")
