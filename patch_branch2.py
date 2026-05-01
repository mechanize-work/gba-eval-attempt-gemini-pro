import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# I am fixing the branch offset calculations. 
# Thumb branch: PC is at instruction + 2 (we read PC as PC+4 but then loop adds 2 to it before executing, no wait, the loop reads pipeline[1], then adds 2, then executes. So when executing, PC is instruction + 4.
# Wait, let's look at `step` again.
