import sys

thumb_code = """
    fn execute_thumb_mov_cmp_add_sub_imm(&mut self, instr: u16, bus: &mut dyn Bus) {
        let op = (instr >> 11) & 0x3;
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = (instr & 0xFF) as u32;

        match op {
            0b00 => { // MOV
                self.regs[rd] = imm;
                self.set_nz(self.regs[rd]);
            }
            0b01 => { // CMP
                let (res, c, v) = self.sub_flags(self.regs[rd], imm);
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0b10 => { // ADD
                let (res, c, v) = self.add_flags(self.regs[rd], imm);
                self.regs[rd] = res;
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0b11 => { // SUB
                let (res, c, v) = self.sub_flags(self.regs[rd], imm);
                self.regs[rd] = res;
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            _ => unreachable!(),
        }
    }

    fn execute_thumb_alu(&mut self, instr: u16, bus: &mut dyn Bus) {
        let op = (instr >> 6) & 0xF;
        let rs = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let val_d = self.regs[rd];
        let val_s = self.regs[rs];

        match op {
            0x0 => { // AND
                let res = val_d & val_s;
                self.regs[rd] = res;
                self.set_nz(res);
            }
            0x1 => { // EOR
                let res = val_d ^ val_s;
                self.regs[rd] = res;
                self.set_nz(res);
            }
            0x2 => { // LSL
                let shift = val_s & 0xFF;
                if shift > 0 {
                    let (res, c) = if shift >= 32 {
                        (0, if shift == 32 { (val_d & 1) != 0 } else { false })
                    } else {
                        (val_d << shift, ((val_d >> (32 - shift)) & 1) != 0)
                    };
                    self.regs[rd] = res;
                    self.set_nz(res);
                    self.set_c(c);
                }
            }
            0x3 => { // LSR
                let shift = val_s & 0xFF;
                if shift > 0 {
                    let (res, c) = if shift >= 32 {
                        (0, if shift == 32 { (val_d & 0x8000_0000) != 0 } else { false })
                    } else {
                        (val_d >> shift, ((val_d >> (shift - 1)) & 1) != 0)
                    };
                    self.regs[rd] = res;
                    self.set_nz(res);
                    self.set_c(c);
                }
            }
            0x4 => { // ASR
                let shift = val_s & 0xFF;
                if shift > 0 {
                    let (res, c) = if shift >= 32 {
                        if (val_d & 0x8000_0000) != 0 {
                            (0xFFFFFFFF, true)
                        } else {
                            (0, false)
                        }
                    } else {
                        (((val_d as i32) >> shift) as u32, ((val_d >> (shift - 1)) & 1) != 0)
                    };
                    self.regs[rd] = res;
                    self.set_nz(res);
                    self.set_c(c);
                }
            }
            0x5 => { // ADC
                let (res, c, v) = self.adc_flags(val_d, val_s);
                self.regs[rd] = res;
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0x6 => { // SBC
                let (res, c, v) = self.sbc_flags(val_d, val_s);
                self.regs[rd] = res;
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0x7 => { // ROR
                let shift = val_s & 0xFF;
                if shift > 0 {
                    let shift = shift & 0x1F;
                    let (res, c) = if shift == 0 {
                        (val_d, (val_d & 0x8000_0000) != 0)
                    } else {
                        (val_d.rotate_right(shift), ((val_d >> (shift - 1)) & 1) != 0)
                    };
                    self.regs[rd] = res;
                    self.set_nz(res);
                    self.set_c(c);
                }
            }
            0x8 => { // TST
                let res = val_d & val_s;
                self.set_nz(res);
            }
            0x9 => { // NEG
                let (res, c, v) = self.sub_flags(0, val_s);
                self.regs[rd] = res;
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0xA => { // CMP
                let (res, c, v) = self.sub_flags(val_d, val_s);
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0xB => { // CMN
                let (res, c, v) = self.add_flags(val_d, val_s);
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0xC => { // ORR
                let res = val_d | val_s;
                self.regs[rd] = res;
                self.set_nz(res);
            }
            0xD => { // MUL
                let res = val_d.wrapping_mul(val_s);
                self.regs[rd] = res;
                self.set_nz(res);
            }
            0xE => { // BIC
                let res = val_d & !val_s;
                self.regs[rd] = res;
                self.set_nz(res);
            }
            0xF => { // MVN
                let res = !val_s;
                self.regs[rd] = res;
                self.set_nz(res);
            }
            _ => unreachable!(),
        }
    }

    fn execute_thumb_hi_reg(&mut self, instr: u16, bus: &mut dyn Bus) {
        let op = (instr >> 8) & 0x3;
        let h1 = (instr >> 7) & 1 != 0;
        let h2 = (instr >> 6) & 1 != 0;
        let rs = (((instr >> 3) & 0x7) | if h2 { 8 } else { 0 }) as usize;
        let rd = ((instr & 0x7) | if h1 { 8 } else { 0 }) as usize;

        let val_s = if rs == 15 { self.regs[15].wrapping_add(2) } else { self.regs[rs] }; // or is it just pc? in thumb pc+4
        let val_d = if rd == 15 { self.regs[15].wrapping_add(2) } else { self.regs[rd] }; 
        // Actually PC is read as PC+4

        match op {
            0b00 => { // ADD
                self.regs[rd] = val_d.wrapping_add(val_s);
                if rd == 15 { self.reload_pipeline(); }
            }
            0b01 => { // CMP
                let (res, c, v) = self.sub_flags(val_d, val_s);
                self.set_nz(res);
                self.set_c(c);
                self.set_v(v);
            }
            0b10 => { // MOV
                self.regs[rd] = val_s;
                if rd == 15 { self.reload_pipeline(); }
            }
            0b11 => { // BX
                let val = val_s;
                self.set_t((val & 1) != 0);
                self.regs[15] = val & !1;
                self.reload_pipeline();
            }
            _ => unreachable!(),
        }
    }

    fn execute_thumb_pc_load(&mut self, instr: u16, bus: &mut dyn Bus) {
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = ((instr & 0xFF) as u32) << 2;
        let addr = (self.regs[15] & !2) + imm;
        self.regs[rd] = bus.read32(addr);
    }

    fn execute_thumb_load_store_reg_offset(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let b_bit = (instr >> 10) & 1 != 0;
        let ro = ((instr >> 6) & 0x7) as usize;
        let rb = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let addr = self.regs[rb].wrapping_add(self.regs[ro]);

        if l_bit { // LDR
            if b_bit {
                self.regs[rd] = bus.read8(addr) as u32;
            } else {
                let val = bus.read32(addr & !3);
                self.regs[rd] = val.rotate_right((addr & 3) * 8);
            }
        } else { // STR
            if b_bit {
                bus.write8(addr, self.regs[rd] as u8);
            } else {
                bus.write32(addr & !3, self.regs[rd]);
            }
        }
    }

    fn execute_thumb_load_store_imm_offset(&mut self, instr: u16, bus: &mut dyn Bus) {
        let b_bit = (instr >> 12) & 1 != 0;
        let l_bit = (instr >> 11) & 1 != 0;
        let imm = ((instr >> 6) & 0x1F) as u32;
        let rb = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let offset = if b_bit { imm } else { imm << 2 };
        let addr = self.regs[rb].wrapping_add(offset);

        if l_bit {
            if b_bit {
                self.regs[rd] = bus.read8(addr) as u32;
            } else {
                let val = bus.read32(addr & !3);
                self.regs[rd] = val.rotate_right((addr & 3) * 8);
            }
        } else {
            if b_bit {
                bus.write8(addr, self.regs[rd] as u8);
            } else {
                bus.write32(addr & !3, self.regs[rd]);
            }
        }
    }

    fn execute_thumb_load_store_hw(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let imm = (((instr >> 6) & 0x1F) as u32) << 1;
        let rb = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let addr = self.regs[rb].wrapping_add(imm);

        if l_bit {
            let val = bus.read16(addr & !1) as u32;
            self.regs[rd] = val.rotate_right((addr & 1) * 8);
        } else {
            bus.write16(addr & !1, self.regs[rd] as u16);
        }
    }

    fn execute_thumb_sp_load_store(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = ((instr & 0xFF) as u32) << 2;

        let addr = self.regs[13].wrapping_add(imm);

        if l_bit {
            let val = bus.read32(addr & !3);
            self.regs[rd] = val.rotate_right((addr & 3) * 8);
        } else {
            bus.write32(addr & !3, self.regs[rd]);
        }
    }

    fn execute_thumb_load_address(&mut self, instr: u16, bus: &mut dyn Bus) {
        let sp_bit = (instr >> 11) & 1 != 0;
        let rd = ((instr >> 8) & 0x7) as usize;
        let imm = ((instr & 0xFF) as u32) << 2;

        if sp_bit {
            self.regs[rd] = self.regs[13].wrapping_add(imm);
        } else {
            self.regs[rd] = (self.regs[15] & !2).wrapping_add(imm);
        }
    }

    fn execute_thumb_add_sp(&mut self, instr: u16, bus: &mut dyn Bus) {
        let s_bit = (instr >> 7) & 1 != 0;
        let imm = ((instr & 0x7F) as u32) << 2;

        if s_bit {
            self.regs[13] = self.regs[13].wrapping_sub(imm);
        } else {
            self.regs[13] = self.regs[13].wrapping_add(imm);
        }
    }

    fn execute_thumb_push_pop(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let r_bit = (instr >> 8) & 1 != 0;
        let r_list = instr & 0xFF;

        if l_bit { // POP
            let mut addr = self.regs[13];
            for i in 0..8 {
                if (r_list & (1 << i)) != 0 {
                    self.regs[i] = bus.read32(addr);
                    addr += 4;
                }
            }
            if r_bit {
                let val = bus.read32(addr);
                self.regs[15] = val & !1;
                self.set_t((val & 1) != 0);
                self.reload_pipeline();
                addr += 4;
            }
            self.regs[13] = addr;
        } else { // PUSH
            let num_regs = r_list.count_ones() + if r_bit { 1 } else { 0 };
            let mut addr = self.regs[13].wrapping_sub(num_regs * 4);
            self.regs[13] = addr;
            
            for i in 0..8 {
                if (r_list & (1 << i)) != 0 {
                    bus.write32(addr, self.regs[i]);
                    addr += 4;
                }
            }
            if r_bit {
                bus.write32(addr, self.regs[14]);
            }
        }
    }

    fn execute_thumb_multiple_load_store(&mut self, instr: u16, bus: &mut dyn Bus) {
        let l_bit = (instr >> 11) & 1 != 0;
        let rb = ((instr >> 8) & 0x7) as usize;
        let r_list = instr & 0xFF;

        let mut addr = self.regs[rb];
        let num_regs = if r_list == 0 { 0 } else { r_list.count_ones() };
        
        let start_addr = addr;

        for i in 0..8 {
            if (r_list & (1 << i)) != 0 {
                if l_bit {
                    self.regs[i] = bus.read32(addr);
                } else {
                    bus.write32(addr, self.regs[i]);
                }
                addr = addr.wrapping_add(4);
            }
        }

        // Handle empty r_list edge case? Wait, if r_list == 0, GBA behaves differently but let's stick to basic for now
        if r_list == 0 {
            if l_bit {
                self.regs[15] = bus.read32(addr);
                self.reload_pipeline();
            } else {
                bus.write32(addr, self.regs[15].wrapping_add(2));
            }
            addr = addr.wrapping_add(0x40);
        }

        if !l_bit || (r_list & (1 << rb)) == 0 {
            self.regs[rb] = addr;
        }
    }

    fn execute_thumb_swi(&mut self, instr: u16, bus: &mut dyn Bus) {
        // Not implemented fully, but usually causes an exception
    }
"""

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Replace everything from execute_thumb_mov_cmp_add_sub_imm down to just before execute_arm_data_processing
start = src.find("    fn execute_thumb_mov_cmp_add_sub_imm")
end = src.find("    fn execute_arm_data_processing")
new_src = src[:start] + thumb_code.strip() + "\n\n" + src[end:]

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(new_src)
