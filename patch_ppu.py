import sys

with open("src/ppu/mod.rs", "r") as f:
    src = f.read()

new_src = src.replace("""    pub fn render_scanline(&self, framebuffer: &mut [u32], line: usize) {
        let forced_blank = (self.dispcnt & 0x80) != 0;
        let start = line * 240;
        
        if forced_blank {
            for i in 0..240 {
                framebuffer[start + i] = 0xFF000000; // Black
            }
            return;
        }

        let mode = self.dispcnt & 7;
        
        // Render backdrop color (color 0 of palette 0)
        let c0 = (self.palette[0] as u32) | ((self.palette[1] as u32) << 8);
        let r = (c0 & 0x1F) << 3;
        let g = ((c0 >> 5) & 0x1F) << 3;
        let b = ((c0 >> 10) & 0x1F) << 3;
        let color = 0xFF000000 | (b << 16) | (g << 8) | r;

        for i in 0..240 {
            framebuffer[start + i] = color;
        }

        // TODO: Render BGs and OBJs based on mode
        if mode == 0 {""", """    pub fn render_scanline(&self, framebuffer: &mut [u32], line: usize) {
        let forced_blank = (self.dispcnt & 0x80) != 0;
        let start = line * 240;
        
        if forced_blank {
            for i in 0..240 {
                framebuffer[start + i] = 0xFF000000; // Black
            }
            return;
        }

        let mode = self.dispcnt & 7;
        let mut line_priorities = [4u8; 240];
        
        // Render backdrop color (color 0 of palette 0)
        let c0 = (self.palette[0] as u32) | ((self.palette[1] as u32) << 8);
        let r = (c0 & 0x1F) << 3;
        let g = ((c0 >> 5) & 0x1F) << 3;
        let b = ((c0 >> 10) & 0x1F) << 3;
        let color = 0xFF000000 | (b << 16) | (g << 8) | r;

        for i in 0..240 {
            framebuffer[start + i] = color;
        }

        // TODO: Render BGs and OBJs based on mode
        if mode == 0 {""")

new_src = new_src.replace("""                let char_base = ((bgcnt >> 2) & 3) as u32 * 16384;""", """                let bg_prio = (bgcnt & 3) as u8;
                let char_base = ((bgcnt >> 2) & 3) as u32 * 16384;""")

new_src = new_src.replace("""                for x in 0..240 {
                    let rx = (x as u32 + bghofs as u32) % width;""", """                for x in 0..240 {
                    if bg_prio >= line_priorities[x] { continue; }
                    let rx = (x as u32 + bghofs as u32) % width;""")

new_src = new_src.replace("""                            if color_idx != 0 {
                                let c = (self.palette[color_idx * 2] as u16) | ((self.palette[color_idx * 2 + 1] as u16) << 8);
                                let pr = (c & 0x1F) << 3;
                                let pg = ((c >> 5) & 0x1F) << 3;
                                let pb = ((c >> 10) & 0x1F) << 3;
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                            }""", """                            if color_idx != 0 {
                                let c = (self.palette[color_idx * 2] as u16) | ((self.palette[color_idx * 2 + 1] as u16) << 8);
                                let pr = (c & 0x1F) << 3;
                                let pg = ((c >> 5) & 0x1F) << 3;
                                let pb = ((c >> 10) & 0x1F) << 3;
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                line_priorities[x] = bg_prio;
                            }""")

new_src = new_src.replace("""                            if color_idx != 0 {
                                let pal_idx = (pal_bank as usize) * 16 + color_idx;
                                let c = (self.palette[pal_idx * 2] as u16) | ((self.palette[pal_idx * 2 + 1] as u16) << 8);
                                let pr = (c & 0x1F) << 3;
                                let pg = ((c >> 5) & 0x1F) << 3;
                                let pb = ((c >> 10) & 0x1F) << 3;
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                            }""", """                            if color_idx != 0 {
                                let pal_idx = (pal_bank as usize) * 16 + color_idx;
                                let c = (self.palette[pal_idx * 2] as u16) | ((self.palette[pal_idx * 2 + 1] as u16) << 8);
                                let pr = (c & 0x1F) << 3;
                                let pg = ((c >> 5) & 0x1F) << 3;
                                let pb = ((c >> 10) & 0x1F) << 3;
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                line_priorities[x] = bg_prio;
                            }""")

new_src = new_src.replace("""                let priority = (attr2 >> 10) & 3;
                let pal_bank = (attr2 >> 12) & 0xF;""", """                let priority = ((attr2 >> 10) & 3) as u8;
                let pal_bank = (attr2 >> 12) & 0xF;""")

new_src = new_src.replace("""                        let screen_x = signed_x + local_x;
                        if screen_x >= 0 && screen_x < 240 {
                            let draw_x = if h_flip { width - 1 - local_x } else { local_x };""", """                        let screen_x = signed_x + local_x;
                        if screen_x >= 0 && screen_x < 240 {
                            let sx = screen_x as usize;
                            if priority >= line_priorities[sx] { continue; }
                            let draw_x = if h_flip { width - 1 - local_x } else { local_x };""")

with open("src/ppu/mod.rs", "w") as f:
    f.write(new_src)
