import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

new_src = src.replace("""                    let screen_idx = match screen_size {
                        0 => 0,
                        1 => map_x / 32,
                        2 => map_y / 32,
                        3 => (map_y / 32) * 2 + (map_x / 32),
                        _ => 0,
                    };""", """                    let screen_idx = match screen_size {
                        0 => 0,
                        1 => map_x / 32,
                        2 => map_y / 32,
                        3 => (map_y / 32) * 2 + (map_x / 32),
                        _ => 0,
                    };
                    // Wait, VRAM is 64KB! My VRAM array is 96KB (0x18000). So it's fine.
""")
# Let's check sprite logic
