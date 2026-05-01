import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

blend_vars = """
        let effect = (self.bldcnt >> 6) & 3;
        let target1 = self.bldcnt & 0x3F;
        let target2 = (self.bldcnt >> 8) & 0x3F;
        let eva = (self.bldalpha & 0x1F).min(16) as u32;
        let evb = ((self.bldalpha >> 8) & 0x1F).min(16) as u32;
        let evy = (self.bldy & 0x1F).min(16) as u32;
"""

src = src.replace('let mut line_priorities = [4u8; 240];', 'let mut line_priorities = [4u8; 240];\n        let mut line_layers = [5u8; 240];\n' + blend_vars)

blend_macro = """
macro_rules! blend_and_draw {
    ($fb:expr, $idx:expr, $pr:expr, $pg:expr, $pb:expr, $layer:expr, $prio:expr) => {
        let is_t1 = (target1 & (1 << $layer)) != 0;
        let is_t2 = (target2 & (1 << line_layers[$idx])) != 0;
        let mut final_r = $pr as u32;
        let mut final_g = $pg as u32;
        let mut final_b = $pb as u32;
        
        if is_t1 && effect != 0 {
            if effect == 1 && is_t2 {
                let old_c = $fb[start + $idx];
                let old_r = (old_c & 0xFF) >> 3;
                let old_g = ((old_c >> 8) & 0xFF) >> 3;
                let old_b = ((old_c >> 16) & 0xFF) >> 3;
                let mut r5 = (final_r >> 3) * eva + old_r * evb;
                let mut g5 = (final_g >> 3) * eva + old_g * evb;
                let mut b5 = (final_b >> 3) * eva + old_b * evb;
                r5 = (r5 / 16).min(31);
                g5 = (g5 / 16).min(31);
                b5 = (b5 / 16).min(31);
                final_r = (r5 << 3) | (r5 >> 2);
                final_g = (g5 << 3) | (g5 >> 2);
                final_b = (b5 << 3) | (b5 >> 2);
            } else if effect == 2 {
                final_r = final_r + ((255 - final_r) * evy / 16);
                final_g = final_g + ((255 - final_g) * evy / 16);
                final_b = final_b + ((255 - final_b) * evy / 16);
            } else if effect == 3 {
                final_r = final_r - (final_r * evy / 16);
                final_g = final_g - (final_g * evy / 16);
                final_b = final_b - (final_b * evy / 16);
            }
        }
        $fb[start + $idx] = 0xFF000000 | (final_b << 16) | (final_g << 8) | final_r;
        line_layers[$idx] = $layer;
        line_priorities[$idx] = $prio;
    }
}
"""

src = src.replace('// Render backdrop color', blend_macro + '\n        // Render backdrop color')

src = src.replace('framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);\n                                line_priorities[x] = bg_prio;', 'blend_and_draw!(framebuffer, x, pr, pg, pb, bg, bg_prio);')

src = src.replace('framebuffer[start + screen_x as usize] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);\n                                        }', 'blend_and_draw!(framebuffer, screen_x as usize, pr, pg, pb, 4, priority);\n                                        }')

bd_blend = """
        let is_t1 = (target1 & (1 << 5)) != 0;
        let mut final_r = r as u32;
        let mut final_g = g as u32;
        let mut final_b = b as u32;
        if is_t1 && effect != 0 {
            if effect == 2 {
                final_r = final_r + ((255 - final_r) * evy / 16);
                final_g = final_g + ((255 - final_g) * evy / 16);
                final_b = final_b + ((255 - final_b) * evy / 16);
            } else if effect == 3 {
                final_r = final_r - (final_r * evy / 16);
                final_g = final_g - (final_g * evy / 16);
                final_b = final_b - (final_b * evy / 16);
            }
        }
        let color = 0xFF000000 | (final_b << 16) | (final_g << 8) | final_r;
"""
src = src.replace('let color = 0xFF000000 | ((b as u32) << 16) | ((g as u32) << 8) | (r as u32);', bd_blend)

with open("src/ppu/mod.rs", "w") as f:
    f.write(src)
