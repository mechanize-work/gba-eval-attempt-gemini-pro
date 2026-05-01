pub struct Ppu {
    pub vram: Box<[u8; 96 * 1024]>,
    pub palette: Box<[u8; 1024]>,
    pub oam: Box<[u8; 1024]>,
    pub dispcnt: u16,
    pub dispstat: u16,
    pub vcount: u16,
    pub bg0cnt: u16,
    pub bg1cnt: u16,
    pub bg2cnt: u16,
    pub bg3cnt: u16,
    pub bg0hofs: u16,
    pub bg0vofs: u16,
    pub bg1hofs: u16,
    pub bg1vofs: u16,
    pub bg2hofs: u16,
    pub bg2vofs: u16,
    pub bg3hofs: u16,
    pub bg3vofs: u16,
    pub keyinput: u16,
}

impl Ppu {
    pub fn new() -> Self {
        Self {
            vram: Box::new([0; 96 * 1024]),
            palette: Box::new([0; 1024]),
            oam: Box::new([0; 1024]),
            dispcnt: 0x0080, // Forced blank by default on power-on
            dispstat: 0,
            vcount: 0,
            bg0cnt: 0,
            bg1cnt: 0,
            bg2cnt: 0,
            bg3cnt: 0,
            bg0hofs: 0,
            bg0vofs: 0,
            bg1hofs: 0,
            bg1vofs: 0,
            bg2hofs: 0,
            bg2vofs: 0,
            bg3hofs: 0,
            bg3vofs: 0,
            keyinput: 0x03FF, // All unpressed by default
        }
    }

    pub fn read8(&self, addr: u32) -> u8 {
        match addr {
            0x04000000 => self.dispcnt as u8,
            0x04000001 => (self.dispcnt >> 8) as u8,
            0x04000004 => self.dispstat as u8,
            0x04000005 => (self.dispstat >> 8) as u8,
            0x04000006 => { println!("VCOUNT READ!"); self.vcount as u8 },
            0x04000007 => (self.vcount >> 8) as u8,
            0x04000008 => self.bg0cnt as u8,
            0x04000009 => (self.bg0cnt >> 8) as u8,
            0x0400000A => self.bg1cnt as u8,
            0x0400000B => (self.bg1cnt >> 8) as u8,
            0x0400000C => self.bg2cnt as u8,
            0x0400000D => (self.bg2cnt >> 8) as u8,
            0x0400000E => self.bg3cnt as u8,
            0x0400000F => (self.bg3cnt >> 8) as u8,
            0x04000130 => self.keyinput as u8,
            0x04000131 => (self.keyinput >> 8) as u8,
            // Offset registers are write-only, but sometimes readable in some emulators as 0
            _ => 0,
        }
    }

    pub fn write8(&mut self, addr: u32, val: u8) {
        match addr {
            0x04000000 => {
                self.dispcnt = (self.dispcnt & 0xFF00) | (val as u16);
                println!("DISPCNT written: {:04X}", self.dispcnt);
            },
            0x04000001 => {
                self.dispcnt = (self.dispcnt & 0x00FF) | ((val as u16) << 8);
                println!("DISPCNT written: {:04X}", self.dispcnt);
            },
            0x04000004 => self.dispstat = (self.dispstat & 0xFF00) | (val as u16),
            0x04000005 => self.dispstat = (self.dispstat & 0x00FF) | ((val as u16) << 8),
            0x04000008 => self.bg0cnt = (self.bg0cnt & 0xFF00) | (val as u16),
            0x04000009 => self.bg0cnt = (self.bg0cnt & 0x00FF) | ((val as u16) << 8),
            0x0400000A => self.bg1cnt = (self.bg1cnt & 0xFF00) | (val as u16),
            0x0400000B => self.bg1cnt = (self.bg1cnt & 0x00FF) | ((val as u16) << 8),
            0x0400000C => self.bg2cnt = (self.bg2cnt & 0xFF00) | (val as u16),
            0x0400000D => self.bg2cnt = (self.bg2cnt & 0x00FF) | ((val as u16) << 8),
            0x0400000E => self.bg3cnt = (self.bg3cnt & 0xFF00) | (val as u16),
            0x0400000F => self.bg3cnt = (self.bg3cnt & 0x00FF) | ((val as u16) << 8),
            0x04000010 => self.bg0hofs = (self.bg0hofs & 0xFF00) | (val as u16),
            0x04000011 => self.bg0hofs = (self.bg0hofs & 0x00FF) | ((val as u16) << 8),
            0x04000012 => self.bg0vofs = (self.bg0vofs & 0xFF00) | (val as u16),
            0x04000013 => self.bg0vofs = (self.bg0vofs & 0x00FF) | ((val as u16) << 8),
            0x04000014 => self.bg1hofs = (self.bg1hofs & 0xFF00) | (val as u16),
            0x04000015 => self.bg1hofs = (self.bg1hofs & 0x00FF) | ((val as u16) << 8),
            0x04000016 => self.bg1vofs = (self.bg1vofs & 0xFF00) | (val as u16),
            0x04000017 => self.bg1vofs = (self.bg1vofs & 0x00FF) | ((val as u16) << 8),
            0x04000018 => self.bg2hofs = (self.bg2hofs & 0xFF00) | (val as u16),
            0x04000019 => self.bg2hofs = (self.bg2hofs & 0x00FF) | ((val as u16) << 8),
            0x0400001A => self.bg2vofs = (self.bg2vofs & 0xFF00) | (val as u16),
            0x0400001B => self.bg2vofs = (self.bg2vofs & 0x00FF) | ((val as u16) << 8),
            0x0400001C => self.bg3hofs = (self.bg3hofs & 0xFF00) | (val as u16),
            0x0400001D => self.bg3hofs = (self.bg3hofs & 0x00FF) | ((val as u16) << 8),
            0x0400001E => self.bg3vofs = (self.bg3vofs & 0xFF00) | (val as u16),
            0x0400001F => self.bg3vofs = (self.bg3vofs & 0x00FF) | ((val as u16) << 8),
            _ => {}
        }
    }

    pub fn render_scanline(&self, framebuffer: &mut [u32], line: usize) {
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
        let r0 = c0 & 0x1F;
        let g0 = (c0 >> 5) & 0x1F;
        let b0 = (c0 >> 10) & 0x1F;
        let r = (r0 << 3) | (r0 >> 2);
        let g = (g0 << 3) | (g0 >> 2);
        let b = (b0 << 3) | (b0 >> 2);
        let color = 0xFF000000 | ((b as u32) << 16) | ((g as u32) << 8) | (r as u32);

        for i in 0..240 {
            framebuffer[start + i] = color;
        }

        // TODO: Render BGs and OBJs based on mode
        if mode == 0 {
            // Mode 0: up to 4 text backgrounds
            for bg in (0..4).rev() { // priority roughly back to front
                let enabled = (self.dispcnt & (1 << (8 + bg))) != 0;
                if !enabled { continue; }
                
                let (bgcnt, bghofs, bgvofs) = match bg {
                    0 => (self.bg0cnt, self.bg0hofs, self.bg0vofs),
                    1 => (self.bg1cnt, self.bg1hofs, self.bg1vofs),
                    2 => (self.bg2cnt, self.bg2hofs, self.bg2vofs),
                    3 => (self.bg3cnt, self.bg3hofs, self.bg3vofs),
                    _ => unreachable!(),
                };

                let bg_prio = (bgcnt & 3) as u8;
                let char_base = ((bgcnt >> 2) & 3) as u32 * 16384;
                let screen_base = ((bgcnt >> 8) & 0x1F) as u32 * 2048;
                let color_mode_256 = (bgcnt & 0x80) != 0;
                
                // Screen size: 00=256x256, 01=512x256, 10=256x512, 11=512x512
                let screen_size = (bgcnt >> 14) & 3;
                let width = if screen_size == 1 || screen_size == 3 { 512 } else { 256 };
                let height = if screen_size == 2 || screen_size == 3 { 512 } else { 256 };

                let y = (line as u32 + bgvofs as u32) % height;
                let map_y = y / 8;
                let tile_y = y % 8;

                for x in 0..240 {
                    if bg_prio >= line_priorities[x] { continue; }
                    let rx = (x as u32 + bghofs as u32) % width;
                    let map_x = rx / 8;
                    let tile_x = rx % 8;

                    let screen_idx = match screen_size {
                        0 => 0,
                        1 => map_x / 32,
                        2 => map_y / 32,
                        3 => (map_y / 32) * 2 + (map_x / 32),
                        _ => 0,
                    };

                    let map_addr = screen_base + screen_idx * 2048 + ((map_y % 32) * 32 + (map_x % 32)) * 2;
                    let map_val = (self.vram[map_addr as usize] as u16) | ((self.vram[map_addr as usize + 1] as u16) << 8);

                    let tile_num = map_val & 0x3FF;
                    let h_flip = (map_val & 0x0400) != 0;
                    let v_flip = (map_val & 0x0800) != 0;
                    let pal_bank = (map_val >> 12) & 0xF;

                    let actual_tx = if h_flip { 7 - tile_x } else { tile_x };
                    let actual_ty = if v_flip { 7 - tile_y } else { tile_y };

                    if color_mode_256 {
                        let tile_addr = char_base + (tile_num as u32) * 64 + actual_ty * 8 + actual_tx;
                        if tile_addr < 96 * 1024 {
                            let color_idx = self.vram[tile_addr as usize] as usize;
                            if color_idx != 0 {
                                let c = (self.palette[color_idx * 2] as u16) | ((self.palette[color_idx * 2 + 1] as u16) << 8);
                                let r = c & 0x1F;
                                let g = (c >> 5) & 0x1F;
                                let b = (c >> 10) & 0x1F;
                                let pr = (r << 3) | (r >> 2);
                                let pg = (g << 3) | (g >> 2);
                                let pb = (b << 3) | (b >> 2);
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                line_priorities[x] = bg_prio;
                            }
                        }
                    } else {
                        let tile_addr = char_base + (tile_num as u32) * 32 + actual_ty * 4 + actual_tx / 2;
                        if tile_addr < 96 * 1024 {
                            let byte = self.vram[tile_addr as usize];
                            let color_idx = if actual_tx % 2 == 0 { byte & 0xF } else { byte >> 4 } as usize;
                            if color_idx != 0 {
                                let pal_idx = (pal_bank as usize) * 16 + color_idx;
                                let c = (self.palette[pal_idx * 2] as u16) | ((self.palette[pal_idx * 2 + 1] as u16) << 8);
                                let r = c & 0x1F;
                                let g = (c >> 5) & 0x1F;
                                let b = (c >> 10) & 0x1F;
                                let pr = (r << 3) | (r >> 2);
                                let pg = (g << 3) | (g >> 2);
                                let pb = (b << 3) | (b >> 2);
                                framebuffer[start + x] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                line_priorities[x] = bg_prio;
                            }
                        }
                    }
                }
            }
        } else if mode == 3 {
            // Mode 3 is a single 240x160 16-bit bitmap
            for i in 0..240 {
                let pixel_offset = (line * 240 + i) * 2;
                if pixel_offset + 1 < self.vram.len() {
                    let pixel = (self.vram[pixel_offset] as u16) | ((self.vram[pixel_offset + 1] as u16) << 8);
                    let pr = (pixel & 0x1F) << 3;
                    let pg = ((pixel >> 5) & 0x1F) << 3;
                    let pb = ((pixel >> 10) & 0x1F) << 3;
                    framebuffer[start + i] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                }
            }
        } else if mode == 4 {
            // Mode 4 is a single 240x160 8-bit bitmap (uses palette)
            let page = (self.dispcnt >> 4) & 1;
            let page_offset = if page == 1 { 0xA000 } else { 0 };
            for i in 0..240 {
                let pixel_offset = page_offset + line * 240 + i;
                if pixel_offset < self.vram.len() {
                    let color_idx = self.vram[pixel_offset] as usize;
                    if color_idx > 0 {
                        let c = (self.palette[color_idx * 2] as u16) | ((self.palette[color_idx * 2 + 1] as u16) << 8);
                        let pr = (c & 0x1F) << 3;
                        let pg = ((c >> 5) & 0x1F) << 3;
                        let pb = ((c >> 10) & 0x1F) << 3;
                        framebuffer[start + i] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                    }
                }
            }
        }

        // Render OBJs (Sprites)
        if (self.dispcnt & 0x1000) != 0 {
            let mapping_1d = (self.dispcnt & 0x40) != 0;
            // Iterate OBJs backwards so lower priority (lower OAM index) draws on top
            for obj_idx in (0..128).rev() {
                let oam_addr = obj_idx * 8;
                let attr0 = (self.oam[oam_addr] as u16) | ((self.oam[oam_addr + 1] as u16) << 8);
                let attr1 = (self.oam[oam_addr + 2] as u16) | ((self.oam[oam_addr + 3] as u16) << 8);
                let attr2 = (self.oam[oam_addr + 4] as u16) | ((self.oam[oam_addr + 5] as u16) << 8);

                let y = attr0 & 0xFF;
                let affine = (attr0 & 0x0100) != 0;
                let double_size_or_disable = (attr0 & 0x0200) != 0;
                
                if !affine && double_size_or_disable {
                    continue; // Disabled
                }

                let mode = (attr0 >> 10) & 3;
                if mode == 3 { continue; } // Prohibited

                let mosaic = (attr0 & 0x1000) != 0;
                let color_mode_256 = (attr0 & 0x2000) != 0;
                let shape = (attr0 >> 14) & 3;

                let x = attr1 & 0x1FF;
                // Affine / Flip
                // Affine not fully implemented yet, just simple rendering
                let h_flip = !affine && (attr1 & 0x1000) != 0;
                let v_flip = !affine && (attr1 & 0x2000) != 0;
                let size = (attr1 >> 14) & 3;

                let tile_num = attr2 & 0x3FF;
                let priority = ((attr2 >> 10) & 3) as u8;
                let pal_bank = (attr2 >> 12) & 0xF;

                let (width, height) = match (shape, size) {
                    (0, 0) => (8, 8),
                    (0, 1) => (16, 16),
                    (0, 2) => (32, 32),
                    (0, 3) => (64, 64),
                    (1, 0) => (16, 8),
                    (1, 1) => (32, 8),
                    (1, 2) => (32, 16),
                    (1, 3) => (64, 32),
                    (2, 0) => (8, 16),
                    (2, 1) => (8, 32),
                    (2, 2) => (16, 32),
                    (2, 3) => (32, 64),
                    _ => (8, 8),
                };

                let signed_y = if y >= 128 { y as i32 - 256 } else { y as i32 };
                let signed_x = if x >= 256 { x as i32 - 512 } else { x as i32 };

                let current_line = line as i32;
                if current_line >= signed_y && current_line < signed_y + height {
                    let mut local_y = current_line - signed_y;
                    if v_flip {
                        local_y = height - 1 - local_y;
                    }

                    for mut local_x in 0..width {
                        let screen_x = signed_x + local_x;
                        if screen_x >= 0 && screen_x < 240 {
                            let sx = screen_x as usize;
                            if priority >= line_priorities[sx] { continue; }
                            let draw_x = if h_flip { width - 1 - local_x } else { local_x };

                            let tile_x = draw_x / 8;
                            let tile_y = local_y / 8;
                            let in_tile_x = draw_x % 8;
                            let in_tile_y = local_y % 8;

                            let tile_offset = if mapping_1d {
                                let offset_multiplier = if color_mode_256 { 2 } else { 1 };
                                (tile_y * (width / 8) + tile_x) * offset_multiplier
                            } else {
                                let offset_multiplier = if color_mode_256 { 2 } else { 1 };
                                tile_y * 32 + tile_x * offset_multiplier
                            };

                            let final_tile = (tile_num + tile_offset as u16) & 0x3FF;

                            let base_addr = 0x10000 + final_tile as u32 * 32;
                            if base_addr < 96 * 1024 {
                                if color_mode_256 {
                                    let addr = base_addr * 2 + (in_tile_y * 8 + in_tile_x) as u32;
                                    if addr < 96 * 1024 {
                                        let color_idx = self.vram[addr as usize] as usize;
                                        if color_idx != 0 {
                                            let c = (self.palette[0x200 + color_idx * 2] as u16) | ((self.palette[0x200 + color_idx * 2 + 1] as u16) << 8);
                                            let r = c & 0x1F;
                                            let g = (c >> 5) & 0x1F;
                                            let b = (c >> 10) & 0x1F;
                                            let pr = (r << 3) | (r >> 2);
                                            let pg = (g << 3) | (g >> 2);
                                            let pb = (b << 3) | (b >> 2);
                                            framebuffer[start + screen_x as usize] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                        }
                                    }
                                } else {
                                    let addr = base_addr + (in_tile_y * 4 + in_tile_x / 2) as u32;
                                    if addr < 96 * 1024 {
                                        let byte = self.vram[addr as usize];
                                        let color_idx = if in_tile_x % 2 == 0 { byte & 0xF } else { byte >> 4 } as usize;
                                        if color_idx != 0 {
                                            let pal_idx = (pal_bank as usize) * 16 + color_idx;
                                            let c = (self.palette[0x200 + pal_idx * 2] as u16) | ((self.palette[0x200 + pal_idx * 2 + 1] as u16) << 8);
                                            let r = c & 0x1F;
                                            let g = (c >> 5) & 0x1F;
                                            let b = (c >> 10) & 0x1F;
                                            let pr = (r << 3) | (r >> 2);
                                            let pg = (g << 3) | (g >> 2);
                                            let pb = (b << 3) | (b >> 2);
                                            framebuffer[start + screen_x as usize] = 0xFF000000 | ((pb as u32) << 16) | ((pg as u32) << 8) | (pr as u32);
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
