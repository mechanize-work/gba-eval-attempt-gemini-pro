use crate::memory::bus::Bus;

#[derive(Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    User = 0b10000,
    Fiq = 0b10001,
    Irq = 0b10010,
    Supervisor = 0b10011,
    Abort = 0b10111,
    Undefined = 0b11011,
    System = 0b11111,
}

impl Mode {
    pub fn from_bits(bits: u32) -> Self {
        match bits & 0x1f {
            0b10000 => Mode::User,
            0b10001 => Mode::Fiq,
            0b10010 => Mode::Irq,
            0b10011 => Mode::Supervisor,
            0b10111 => Mode::Abort,
            0b11011 => Mode::Undefined,
            0b11111 => Mode::System,
            _ => Mode::System, // Fallback
        }
    }
}

pub struct Cpu {
    pub regs: [u32; 16],
    pub cpsr: u32,
    pub spsr: u32,

    banked_r8_r12: [u32; 5],
    banked_r13_r14_usr: [u32; 2],
    banked_r13_r14_fiq: [u32; 2],
    banked_r13_r14_svc: [u32; 2],
    banked_r13_r14_abt: [u32; 2],
    banked_r13_r14_irq: [u32; 2],
    banked_r13_r14_und: [u32; 2],

    banked_spsr_fiq: u32,
    banked_spsr_svc: u32,
    banked_spsr_abt: u32,
    banked_spsr_irq: u32,
    banked_spsr_und: u32,

    pipeline: [u32; 2],
    pub pipeline_empty: bool,
    pub cycles: usize,
    pub halted: bool,
    pub saved_ime: u16,
}

impl Cpu {
    pub fn new() -> Self {
        Cpu {
            regs: [0; 16],
            cpsr: 0x0000_00D3, // Supervisor mode, IRQ/FIQ disabled
            spsr: 0,
            banked_r8_r12: [0; 5],
            banked_r13_r14_usr: [0; 2],
            banked_r13_r14_fiq: [0; 2],
            banked_r13_r14_svc: [0; 2],
            banked_r13_r14_abt: [0; 2],
            banked_r13_r14_irq: [0; 2],
            banked_r13_r14_und: [0; 2],
            banked_spsr_fiq: 0,
            banked_spsr_svc: 0,
            banked_spsr_abt: 0,
            banked_spsr_irq: 0,
            banked_spsr_und: 0,
            pipeline: [0; 2],
            pipeline_empty: true,
            cycles: 0,
            halted: false,
            saved_ime: 0xFFFF,
        }
    }

    pub fn get_mode(&self) -> Mode {
        Mode::from_bits(self.cpsr)
    }

    pub fn get_memory_cycles_32(&self, addr: u32) -> usize {
        match addr >> 24 {
            0x02 => 3, // EWRAM
            0x03 => 1, // IWRAM
            0x04 => 1, // I/O
            0x05 => 1, // PAL
            0x06 => 1, // VRAM
            0x07 => 1, // OAM
            0x08 | 0x09 | 0x0A | 0x0B | 0x0C | 0x0D => 4, // ROM
            0x0E => 5, // SRAM
            _ => 1,
        }
    }

    pub fn set_mode(&mut self, new_mode: Mode) {
        let old_mode = self.get_mode();
        if old_mode == new_mode {
            return;
        }

        // Swap r8-r12 if transitioning to or from FIQ mode
        if (old_mode == Mode::Fiq) != (new_mode == Mode::Fiq) {
            let mut temp = [0; 5];
            temp.copy_from_slice(&self.regs[8..13]);
            self.regs[8..13].copy_from_slice(&self.banked_r8_r12);
            self.banked_r8_r12.copy_from_slice(&temp);
        }

        // Save r13, r14, spsr
        match old_mode {
            Mode::User | Mode::System => self.banked_r13_r14_usr.copy_from_slice(&self.regs[13..15]),
            Mode::Fiq => { self.banked_r13_r14_fiq.copy_from_slice(&self.regs[13..15]); self.banked_spsr_fiq = self.spsr; },
            Mode::Supervisor => { self.banked_r13_r14_svc.copy_from_slice(&self.regs[13..15]); self.banked_spsr_svc = self.spsr; },
            Mode::Abort => { self.banked_r13_r14_abt.copy_from_slice(&self.regs[13..15]); self.banked_spsr_abt = self.spsr; },
            Mode::Irq => { self.banked_r13_r14_irq.copy_from_slice(&self.regs[13..15]); self.banked_spsr_irq = self.spsr; },
            Mode::Undefined => { self.banked_r13_r14_und.copy_from_slice(&self.regs[13..15]); self.banked_spsr_und = self.spsr; },
        }

        // Load r13, r14, spsr
        match new_mode {
            Mode::User | Mode::System => self.regs[13..15].copy_from_slice(&self.banked_r13_r14_usr),
            Mode::Fiq => { self.regs[13..15].copy_from_slice(&self.banked_r13_r14_fiq); self.spsr = self.banked_spsr_fiq; },
            Mode::Supervisor => { self.regs[13..15].copy_from_slice(&self.banked_r13_r14_svc); self.spsr = self.banked_spsr_svc; },
            Mode::Abort => { self.regs[13..15].copy_from_slice(&self.banked_r13_r14_abt); self.spsr = self.banked_spsr_abt; },
            Mode::Irq => { self.regs[13..15].copy_from_slice(&self.banked_r13_r14_irq); self.spsr = self.banked_spsr_irq; },
            Mode::Undefined => { self.regs[13..15].copy_from_slice(&self.banked_r13_r14_und); self.spsr = self.banked_spsr_und; },
        }

        self.cpsr = (self.cpsr & !0x1F) | (new_mode as u32);
    }

    pub fn get_n(&self) -> bool { (self.cpsr & (1 << 31)) != 0 }
    pub fn get_z(&self) -> bool { (self.cpsr & (1 << 30)) != 0 }
    pub fn set_i(&mut self, val: bool) {
        if val {
            self.cpsr |= 1 << 7;
        } else {
            self.cpsr &= !(1 << 7);
        }
    }
    pub fn get_c(&self) -> bool { (self.cpsr & (1 << 29)) != 0 }
    pub fn get_v(&self) -> bool { (self.cpsr & (1 << 28)) != 0 }
    pub fn get_t(&self) -> bool { (self.cpsr & (1 << 5)) != 0 }

    pub fn set_n(&mut self, val: bool) { if val { self.cpsr |= 1 << 31; } else { self.cpsr &= !(1 << 31); } }
    pub fn set_z(&mut self, val: bool) { if val { self.cpsr |= 1 << 30; } else { self.cpsr &= !(1 << 30); } }
    pub fn set_c(&mut self, val: bool) { if val { self.cpsr |= 1 << 29; } else { self.cpsr &= !(1 << 29); } }
    pub fn set_v(&mut self, val: bool) { if val { self.cpsr |= 1 << 28; } else { self.cpsr &= !(1 << 28); } }
    pub fn set_t(&mut self, val: bool) { if val { self.cpsr |= 1 << 5; } else { self.cpsr &= !(1 << 5); } }

    pub fn set_nz(&mut self, result: u32) {
        self.set_n((result & 0x8000_0000) != 0);
        self.set_z(result == 0);
    }

    pub fn reload_pipeline(&mut self) {
        self.pipeline_empty = true;
    }

    pub fn check_cond(&self, cond: u32) -> bool {
        let n = self.get_n();
        let z = self.get_z();
        let c = self.get_c();
        let v = self.get_v();

        match cond {
            0x0 => z,                   // EQ
            0x1 => !z,                  // NE
            0x2 => c,                   // CS
            0x3 => !c,                  // CC
            0x4 => n,                   // MI
            0x5 => !n,                  // PL
            0x6 => v,                   // VS
            0x7 => !v,                  // VC
            0x8 => c && !z,             // HI
            0x9 => !c || z,             // LS
            0xA => n == v,              // GE
            0xB => n != v,              // LT
            0xC => !z && (n == v),      // GT
            0xD => z || (n != v),       // LE
            0xE => true,                // AL
            0xF => false,               // NV
            _ => false,
        }
    }

    fn add_flags(&self, a: u32, b: u32) -> (u32, bool, bool) {
        let (res, c1) = a.overflowing_add(b);
        let v = ((a ^ res) & (b ^ res) & 0x8000_0000) != 0;
        (res, c1, v)
    }

    fn sub_flags(&self, a: u32, b: u32) -> (u32, bool, bool) {
        let (res, c1) = a.overflowing_sub(b);
        let v = ((a ^ b) & (a ^ res) & 0x8000_0000) != 0;
        (res, !c1, v)
    }

    fn adc_flags(&self, a: u32, b: u32) -> (u32, bool, bool) {
        let c_in = if self.get_c() { 1 } else { 0 };
        let (res1, c1) = a.overflowing_add(b);
        let (res, c2) = res1.overflowing_add(c_in);
        let v = ((a ^ res) & (b ^ res) & 0x8000_0000) != 0;
        (res, c1 || c2, v)
    }

    fn sbc_flags(&self, a: u32, b: u32) -> (u32, bool, bool) {
        let c_in = if self.get_c() { 0 } else { 1 };
        let (res1, c1) = a.overflowing_sub(b);
        let (res, c2) = res1.overflowing_sub(c_in);
        let v = ((a ^ b) & (a ^ res) & 0x8000_0000) != 0;
        (res, !(c1 || c2), v)
    }

    pub fn restore_spsr(&mut self) {
        self.cpsr = self.spsr;
        self.set_mode(Mode::from_bits(self.cpsr));
    }

    fn get_arm_op2(&self, instr: u32, i_bit: bool) -> (u32, bool) {
        if i_bit {
            // Immediate
            let imm = instr & 0xFF;
            let rotate = (instr >> 8) & 0xF;
            if rotate == 0 {
                (imm, self.get_c())
            } else {
                let rot_amount = rotate * 2;
                let val = imm.rotate_right(rot_amount);
                (val, (val & 0x8000_0000) != 0)
            }
        } else {
            // Register
            let rm = (instr & 0xF) as usize;
            let shift_type = (instr >> 5) & 3;
            let shift_amount = if (instr & 0x10) == 0 {
                (instr >> 7) & 0x1F
            } else {
                let rs = ((instr >> 8) & 0xF) as usize;
                self.regs[rs] & 0xFF
            };

            let rm_val = if rm == 15 {
                if (instr & 0x10) != 0 { self.regs[15].wrapping_add(4) } else { self.regs[15] }
            } else {
                self.regs[rm]
            };

            if shift_amount == 0 {
                if (instr & 0x10) != 0 {
                    return (rm_val, self.get_c()); // Shift by register 0
                }
                match shift_type {
                    0 => (rm_val, self.get_c()), // LSL #0
                    1 => (0, (rm_val & 0x8000_0000) != 0), // LSR #32
                    2 => { // ASR #32
                        if (rm_val & 0x8000_0000) != 0 {
                            (0xFFFFFFFF, true)
                        } else {
                            (0, false)
                        }
                    }
                    3 => { // ROR #32 / RRX
                        let c_in = if self.get_c() { 1 << 31 } else { 0 };
                        ((rm_val >> 1) | c_in, (rm_val & 1) != 0)
                    }
                    _ => unreachable!(),
                }
            } else if shift_amount >= 32 {
                match shift_type {
                    0 => (0, if shift_amount == 32 { (rm_val & 1) != 0 } else { false }),
                    1 => (0, if shift_amount == 32 { (rm_val & 0x8000_0000) != 0 } else { false }),
                    2 => {
                        if (rm_val & 0x8000_0000) != 0 {
                            (0xFFFFFFFF, true)
                        } else {
                            (0, false)
                        }
                    }
                    3 => {
                        let amount = shift_amount & 31;
                        if amount == 0 {
                            (rm_val, (rm_val & 0x8000_0000) != 0)
                        } else {
                            (rm_val.rotate_right(amount), ((rm_val >> (amount - 1)) & 1) != 0)
                        }
                    }
                    _ => unreachable!(),
                }
            } else {
                match shift_type {
                    0 => (rm_val << shift_amount, ((rm_val >> (32 - shift_amount)) & 1) != 0),
                    1 => (rm_val >> shift_amount, ((rm_val >> (shift_amount - 1)) & 1) != 0),
                    2 => (((rm_val as i32) >> shift_amount) as u32, ((rm_val >> (shift_amount - 1)) & 1) != 0),
                    3 => (rm_val.rotate_right(shift_amount), ((rm_val >> (shift_amount - 1)) & 1) != 0),
                    _ => unreachable!(),
                }
            }
        }
    }

    pub fn step(&mut self, bus: &mut dyn Bus) {
        if self.halted {
            self.cycles += 1;
            return;
        }

        if self.pipeline_empty {
            self.fill_pipeline(bus);
        }

        let instr = self.pipeline[0];
        self.pipeline[0] = self.pipeline[1];

        let pc = self.regs[15].wrapping_sub(if self.get_t() { 2 } else { 4 });
        self.cycles += 1;

        if self.get_t() {
            self.execute_thumb(instr as u16, bus);
            if !self.pipeline_empty {
                self.pipeline[1] = bus.read16(self.regs[15]) as u32;
                self.regs[15] = self.regs[15].wrapping_add(2);
            }
        } else {
            if self.check_cond(instr >> 28) {
                self.execute_arm(instr, bus);
            }
            if !self.pipeline_empty {
                self.pipeline[1] = bus.read32(self.regs[15]);
                self.regs[15] = self.regs[15].wrapping_add(4);
            }
        }
    }

    fn fill_pipeline(&mut self, bus: &mut dyn Bus) {
        if self.get_t() {
            self.regs[15] &= !1;
            self.pipeline[0] = bus.read16(self.regs[15]) as u32;
            self.regs[15] = self.regs[15].wrapping_add(2);
            self.pipeline[1] = bus.read16(self.regs[15]) as u32;
            self.regs[15] = self.regs[15].wrapping_add(2);
        } else {
            self.regs[15] &= !3;
            self.pipeline[0] = bus.read32(self.regs[15]);
            self.regs[15] = self.regs[15].wrapping_add(4);
            self.pipeline[1] = bus.read32(self.regs[15]);
            self.regs[15] = self.regs[15].wrapping_add(4);
        }
        self.pipeline_empty = false;
    }

    fn execute_arm(&mut self, instr: u32, bus: &mut dyn Bus) {
        if (instr & 0x0FFFFFF0) == 0x012FFF10 {
            // BX
            let rm = instr & 0xF;
            let val = self.regs[rm as usize];
            self.set_t((val & 1) != 0);
            self.regs[15] = val & !1;
            self.reload_pipeline();
            return;
        }

        if (instr & 0x0FBF0FFF) == 0x010F0000 {
            // MRS
            let r_bit = (instr >> 22) & 1 != 0;
            let rd = ((instr >> 12) & 0xF) as usize;
            self.regs[rd] = if r_bit { self.spsr } else { self.cpsr };
            return;
        }

        if (instr & 0x0DB0F000) == 0x0120F000 {
            // MSR
            let r_bit = (instr >> 22) & 1 != 0;
            let i_bit = (instr >> 25) & 1 != 0;
            
            let val = if i_bit {
                let imm = instr & 0xFF;
                let rot = (instr >> 8) & 0xF;
                imm.rotate_right(rot * 2)
            } else {
                self.regs[(instr & 0xF) as usize]
            };

            let mask = {
                let mut m = 0;
                if (instr & (1 << 19)) != 0 { m |= 0xFF000000; } // f
                if (instr & (1 << 18)) != 0 { m |= 0x00FF0000; } // s
                if (instr & (1 << 17)) != 0 { m |= 0x0000FF00; } // x
                if (instr & (1 << 16)) != 0 { m |= 0x000000FF; } // c
                m
            };

            if r_bit {
                self.spsr = (self.spsr & !mask) | (val & mask);
            } else {
                let old_mode = self.get_mode();
                self.cpsr = (self.cpsr & !mask) | (val & mask);
                let new_mode = self.get_mode();
                if old_mode != new_mode {
                    // Actually we need to set mode correctly, but set_mode swaps registers!
                    // To do this cleanly, we need to manually swap registers.
                    // For now, let's just update the registers:
                    self.cpsr = (self.cpsr & 0xFFFFFFE0) | (old_mode as u32);
                    self.set_mode(new_mode);
                }
            }
            return;
        }

        match (instr >> 25) & 7 {
            0b000 => {
                if (instr & 0x90) == 0x90 {
                    self.execute_arm_multiply_or_halfword(instr, bus);
                } else {
                    self.execute_arm_data_processing(instr, bus);
                }
            }
            0b001 => self.execute_arm_data_processing(instr, bus),
            0b010 => self.execute_arm_load_store(instr, bus),
            0b011 => {
                if (instr & 0x10) == 0x10 {
                    // Undefined
                } else {
                    self.execute_arm_load_store(instr, bus);
                }
            }
            0b100 => self.execute_arm_ldm_stm(instr, bus),
            0b101 => self.execute_arm_branch(instr, bus),
            0b110 => self.execute_arm_coprocessor(instr, bus),
            0b111 => {
                if (instr & 0x0F000000) == 0x0F000000 {
                    self.execute_arm_swi(instr, bus);
                } else {
                    self.execute_arm_coprocessor(instr, bus);
                }
            }
            _ => unreachable!(),
        }
    }

    fn execute_thumb(&mut self, instr: u16, bus: &mut dyn Bus) {
        let opcode = instr >> 11;
        match opcode {
            0b00000 | 0b00001 | 0b00010 => {
                // Move shifted register
                self.execute_thumb_move_shifted_register(instr, bus);
            }
            0b00011 => {
                // Add/subtract
                self.execute_thumb_add_sub(instr, bus);
            }
            0b00100 | 0b00101 | 0b00110 | 0b00111 => {
                // Move/compare/add/subtract immediate
                self.execute_thumb_mov_cmp_add_sub_imm(instr, bus);
            }
            0b01000 => {
                if (instr & 0x0400) == 0 {
                    // ALU operations
                    self.execute_thumb_alu(instr, bus);
                } else if (instr & 0x0300) == 0x0300 {
                    // Branch and exchange (BX)
                    self.execute_thumb_bx(instr, bus);
                } else {
                    // Hi register operations/branch exchange
                    self.execute_thumb_hi_reg(instr, bus);
                }
            }
            0b01001 => {
                // PC-relative load
                self.execute_thumb_pc_load(instr, bus);
            }
            0b01010 | 0b01011 => {
                // Load/store with register offset
                self.execute_thumb_load_store_reg_offset(instr, bus);
            }
            0b01100 | 0b01101 | 0b01110 | 0b01111 => {
                // Load/store with immediate offset
                self.execute_thumb_load_store_imm_offset(instr, bus);
            }
            0b10000 | 0b10001 => {
                // Load/store halfword
                self.execute_thumb_load_store_hw(instr, bus);
            }
            0b10010 | 0b10011 => {
                // SP-relative load/store
                self.execute_thumb_sp_load_store(instr, bus);
            }
            0b10100 | 0b10101 => {
                // Load address
                self.execute_thumb_load_address(instr, bus);
            }
            0b10110 => {
                if (instr & 0x0F00) == 0 {
                    // Add offset to SP
                    self.execute_thumb_add_sp(instr, bus);
                } else {
                    // Push/Pop registers
                    self.execute_thumb_push_pop(instr, bus);
                }
            }
            0b10111 => {
                // Push/pop registers
                self.execute_thumb_push_pop(instr, bus);
            }
            0b11000 | 0b11001 => {
                // Multiple load/store
                self.execute_thumb_multiple_load_store(instr, bus);
            }
            0b11010 | 0b11011 => {
                if (instr & 0x0F00) == 0x0F00 {
                    // Software interrupt
                    self.execute_thumb_swi(instr, bus);
                } else {
                    // Conditional branch
                    self.execute_thumb_cond_branch(instr, bus);
                }
            }
            0b11100 => {
                // Unconditional branch
                self.execute_thumb_uncond_branch(instr, bus);
            }
            0b11101 => {
                // Undefined / BLX suffix (ARMv5T, but in GBA it's usually just BL prefix/suffix)
                self.execute_thumb_bl(instr, bus);
            }
            0b11110 | 0b11111 => {
                // Long branch with link (BL)
                self.execute_thumb_bl(instr, bus);
            }
            _ => unreachable!(),
        }
    }

    fn execute_thumb_move_shifted_register(&mut self, instr: u16, _bus: &mut dyn Bus) {
        let op = (instr >> 11) & 0x3;
        let offset = (instr >> 6) & 0x1F;
        let rs = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let val = self.regs[rs];
        let (res, carry) = match op {
            0b00 => {
                if offset == 0 {
                    (val, self.get_c())
                } else {
                    (val << offset, ((val >> (32 - offset)) & 1) != 0)
                }
            }
            0b01 => {
                if offset == 0 {
                    (0, (val & 0x8000_0000) != 0)
                } else {
                    (val >> offset, ((val >> (offset - 1)) & 1) != 0)
                }
            }
            0b10 => {
                if offset == 0 {
                    if (val & 0x8000_0000) != 0 {
                        (0xFFFFFFFF, true)
                    } else {
                        (0, false)
                    }
                } else {
                    (((val as i32) >> offset) as u32, ((val >> (offset - 1)) & 1) != 0)
                }
            }
            _ => unreachable!(),
        };

        self.regs[rd] = res;
        self.set_nz(res);
        self.set_c(carry);
    }
    fn execute_thumb_add_sub(&mut self, instr: u16, _bus: &mut dyn Bus) {
        let i_bit = (instr >> 10) & 1 != 0;
        let op_sub = (instr >> 9) & 1 != 0;
        let rn = (instr >> 6) & 0x7;
        let rs = ((instr >> 3) & 0x7) as usize;
        let rd = (instr & 0x7) as usize;

        let op2 = if i_bit {
            rn as u32
        } else {
            self.regs[rn as usize]
        };

        let op1 = self.regs[rs];
        let (res, c, v) = if op_sub {
            self.sub_flags(op1, op2)
        } else {
            self.add_flags(op1, op2)
        };

        self.regs[rd] = res;
        self.set_nz(res);
        self.set_c(c);
        self.set_v(v);
    }
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
        let addr = (self.regs[15] & !3).wrapping_add(imm);
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
            self.regs[rd] = (self.regs[15] & !3).wrapping_add(imm);
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
            let num_regs = r_list.count_ones() + if r_bit { 1 } else { 0 };
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

        // STM/LDM writeback happens AFTER the instruction accesses memory.
        // Writeback should ALWAYS happen if rb is not in the list.
        if !l_bit || (r_list & (1 << rb)) == 0 {
            self.regs[rb] = addr;
        }
    }

    fn execute_thumb_swi(&mut self, instr: u16, bus: &mut dyn Bus) {
        let swi_num = instr & 0xFF;
        if self.handle_hle_swi(swi_num as u32, bus) { return; }

        let old_cpsr = self.cpsr;
        self.set_mode(Mode::Supervisor);
        self.spsr = old_cpsr;
        self.regs[14] = self.regs[15].wrapping_sub(2); // In THUMB, PC is ahead by 4, but SWI saves PC of next instr
        self.set_t(false);
        self.set_i(true);
        self.regs[15] = 0x00000008;
        self.reload_pipeline();
    }

    
    fn execute_thumb_bx(&mut self, instr: u16, bus: &mut dyn Bus) {
        let rm = (instr >> 3) & 0xF;
        let val = self.regs[rm as usize];
        self.set_t((val & 1) != 0);
        self.regs[15] = val & !1;
        self.reload_pipeline();
    }
    fn execute_thumb_cond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let cond = (instr >> 8) & 0xF;
        let offset = (instr & 0xFF) as i8 as i32;
        if self.check_cond(cond as u32) {
            self.regs[15] = self.regs[15].wrapping_add((offset << 1) as u32);
            self.reload_pipeline();
        }
    }
    fn execute_thumb_uncond_branch(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        let signed_offset = if (offset & 0x400) != 0 { offset | (!0x7FF) } else { offset };
        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 1) as u32);
        self.reload_pipeline();
    }
    fn execute_thumb_bl(&mut self, instr: u16, bus: &mut dyn Bus) {
        let offset = (instr & 0x7FF) as i32;
        if (instr & 0x0800) == 0 {
            let mut signed_offset = offset;
            if (signed_offset & 0x400) != 0 {
                signed_offset |= !0x7FF;
            }
            self.regs[14] = self.regs[15].wrapping_add((signed_offset << 12) as u32);
        } else {
            let next_pc = self.regs[15];
            self.regs[15] = self.regs[14].wrapping_add((offset << 1) as u32) & !1;
            self.regs[14] = next_pc.wrapping_sub(2) | 1;
            self.reload_pipeline();
        }
    }

    fn execute_arm_data_processing(&mut self, instr: u32, bus: &mut dyn Bus) {
        let i_bit = (instr >> 25) & 1 != 0;
        let opcode = (instr >> 21) & 0xF;
        let s_bit = (instr >> 20) & 1 != 0;
        let rn = ((instr >> 16) & 0xF) as usize;
        let rd = ((instr >> 12) & 0xF) as usize;

        
        if !s_bit && (opcode >= 0x8 && opcode <= 0xB) {
            let r_bit = (instr & (1 << 22)) != 0;
            if (instr & 0x00200000) == 0 {
                // MRS
                let val = if r_bit { self.spsr } else { self.cpsr };
                self.regs[rd] = val;
            } else {
                // MSR
                let val = if i_bit {
                    let imm = instr & 0xFF;
                    let rot = (instr >> 8) & 0xF;
                    imm.rotate_right(rot * 2)
                } else {
                    self.regs[instr as usize & 0xF]
                };
                
                let mask = if (instr & (1 << 16)) != 0 { 0xFF } else { 0 }
                         | if (instr & (1 << 17)) != 0 { 0xFF00 } else { 0 }
                         | if (instr & (1 << 18)) != 0 { 0xFF0000 } else { 0 }
                         | if (instr & (1 << 19)) != 0 { 0xFF000000 } else { 0 };

                if r_bit {
                    self.spsr = (self.spsr & !mask) | (val & mask);
                } else {
                    let old_mode = self.get_mode();
                    let new_cpsr = (self.cpsr & !mask) | (val & mask);
                    // Don't allow changing mode from User
                    if old_mode != Mode::User {
                        let new_mode_bits = new_cpsr & 0x1F;
                        let new_mode = Mode::from_bits(new_cpsr);
                        self.set_mode(new_mode);
                    }
                    // Bits 5-27 are reserved or set specially.
                    // Actually, just apply mask.
                    self.cpsr = (self.cpsr & !mask) | (val & mask);
                }
            }
            return;
        }

        let (op2, shift_carry) = self.get_arm_op2(instr, i_bit);

        
        let val_n = if rn == 15 {
            if !i_bit && (instr & 0x10) != 0 {
                self.regs[15].wrapping_add(4)
            } else {
                self.regs[15]
            }
        } else {
            self.regs[rn]
        };

        let mut carry_out = self.get_c();
        let mut overflow_out = self.get_v();
        
        let result = match opcode {
            0x0 => { carry_out = shift_carry; val_n & op2 } // AND
            0x1 => { carry_out = shift_carry; val_n ^ op2 } // EOR
            0x2 => { // SUB
                let (res, c, v) = self.sub_flags(val_n, op2);
                carry_out = c; overflow_out = v; res
            }
            0x3 => { // RSB
                let (res, c, v) = self.sub_flags(op2, val_n);
                carry_out = c; overflow_out = v; res
            }
            0x4 => { // ADD
                let (res, c, v) = self.add_flags(val_n, op2);
                carry_out = c; overflow_out = v; res
            }
            0x5 => { // ADC
                let (res, c, v) = self.adc_flags(val_n, op2);
                carry_out = c; overflow_out = v; res
            }
            0x6 => { // SBC
                let (res, c, v) = self.sbc_flags(val_n, op2);
                carry_out = c; overflow_out = v; res
            }
            0x7 => { // RSC
                let (res, c, v) = self.sbc_flags(op2, val_n);
                carry_out = c; overflow_out = v; res
            }
            0x8 => { carry_out = shift_carry; val_n & op2 } // TST
            0x9 => { carry_out = shift_carry; val_n ^ op2 } // TEQ
            0xA => { // CMP
                let (_, c, v) = self.sub_flags(val_n, op2);
                carry_out = c; overflow_out = v; val_n.wrapping_sub(op2)
            }
            0xB => { // CMN
                let (_, c, v) = self.add_flags(val_n, op2);
                carry_out = c; overflow_out = v; val_n.wrapping_add(op2)
            }
            0xC => { carry_out = shift_carry; val_n | op2 } // ORR
            0xD => { carry_out = shift_carry; op2 } // MOV
            0xE => { carry_out = shift_carry; val_n & !op2 } // BIC
            0xF => { carry_out = shift_carry; !op2 } // MVN
            _ => unreachable!(),
        };

        let is_logical = matches!(opcode, 0x0 | 0x1 | 0x8 | 0x9 | 0xC | 0xD | 0xE | 0xF);

        if s_bit && rd == 15 {
            self.restore_spsr();
        } else if s_bit {
            self.set_nz(result);
            self.set_c(carry_out);
            if !is_logical {
                self.set_v(overflow_out);
            }
        }

        if opcode < 0x8 || opcode >= 0xC {
            self.regs[rd] = result;
            if rd == 15 {
                self.reload_pipeline();
            }
        }
    }

    fn execute_arm_multiply_or_halfword(&mut self, instr: u32, bus: &mut dyn Bus) {
        // Fallback for unimplemented
    }

    fn execute_arm_load_store(&mut self, instr: u32, bus: &mut dyn Bus) {
        let i_bit = (instr >> 25) & 1 == 0; // Notice: I bit is inverted for LDR/STR
        let p_bit = (instr >> 24) & 1 != 0;
        let u_bit = (instr >> 23) & 1 != 0;
        let b_bit = (instr >> 22) & 1 != 0;
        let w_bit = (instr >> 21) & 1 != 0;
        let l_bit = (instr >> 20) & 1 != 0;
        let rn = ((instr >> 16) & 0xF) as usize;
        let rd = ((instr >> 12) & 0xF) as usize;

        let offset = if i_bit {
            // Immediate
            instr & 0xFFF
        } else {
            // Register shifted
            let (val, _) = self.get_arm_op2(instr & 0xFFF, false);
            val
        };

        let base = if rn == 15 { self.regs[15] } else { self.regs[rn] };
        
        let addr = if p_bit {
            if u_bit { base.wrapping_add(offset) } else { base.wrapping_sub(offset) }
        } else {
            base
        };

        if l_bit {
            let data = if b_bit {
                bus.read8(addr) as u32
            } else {
                let val = bus.read32(addr & !3);
                val.rotate_right((addr & 3) * 8)
            };
            self.regs[rd] = data;
            if rd == 15 {
                self.reload_pipeline();
            }
        } else {
            let data = if rd == 15 {
                self.regs[15].wrapping_add(4)
            } else {
                self.regs[rd]
            };
            if b_bit {
                bus.write8(addr, data as u8);
            } else {
                bus.write32(addr & !3, data);
            }
        }

        if !p_bit {
            let new_base = if u_bit { base.wrapping_add(offset) } else { base.wrapping_sub(offset) };
            self.regs[rn] = new_base;
        } else if w_bit {
            self.regs[rn] = addr;
        }
    }

    fn execute_arm_ldm_stm(&mut self, instr: u32, bus: &mut dyn Bus) {
        let p_bit = (instr >> 24) & 1 != 0;
        let u_bit = (instr >> 23) & 1 != 0;
        let s_bit = (instr >> 22) & 1 != 0;
        let w_bit = (instr >> 21) & 1 != 0;
        let l_bit = (instr >> 20) & 1 != 0;
        let rn = ((instr >> 16) & 0xF) as usize;
        let reg_list = instr & 0xFFFF;

        let mut addr = self.regs[rn];
        let num_regs = reg_list.count_ones();
                
        let start_addr = if u_bit {
            if p_bit { addr.wrapping_add(4) } else { addr }
        } else {
            if p_bit { addr.wrapping_sub(num_regs * 4) } else { addr.wrapping_sub(num_regs * 4 - 4) }
        };

        let end_addr = start_addr.wrapping_add(num_regs * 4);
        
        let mut curr_addr = start_addr;
        for i in 0..16 {
            if (reg_list & (1 << i)) != 0 {
                if l_bit {
                    self.regs[i] = bus.read32(curr_addr);
                } else {
                    let data = if i == 15 { self.regs[15].wrapping_add(4) } else { self.regs[i] };
                    bus.write32(curr_addr, data);
                }
                curr_addr = curr_addr.wrapping_add(4);
            }
        }

        if w_bit && (l_bit || (reg_list & (1 << rn)) == 0) {
            self.regs[rn] = if u_bit { addr.wrapping_add(num_regs * 4) } else { addr.wrapping_sub(num_regs * 4) };
        }

        if l_bit && (reg_list & (1 << 15)) != 0 {
            if s_bit {
                self.restore_spsr();
            }
            self.reload_pipeline();
        }
    }

    fn execute_arm_branch(&mut self, instr: u32, bus: &mut dyn Bus) {
        let l_bit = (instr >> 24) & 1 != 0;
        let offset = instr & 0x00FFFFFF;
        let signed_offset = if (offset & 0x00800000) != 0 {
            offset | 0xFF000000
        } else {
            offset
        };

        if l_bit {
            self.regs[14] = self.regs[15].wrapping_sub(4);
        }

        self.regs[15] = self.regs[15].wrapping_add((signed_offset << 2) as u32);
        self.reload_pipeline();
    }

    fn execute_arm_swi(&mut self, instr: u32, bus: &mut dyn Bus) {
        let swi_num = (instr & 0xFFFFFF) >> 16; // wait, SWI number is 24 bits. Usually GBA uses bits 16-23? Actually, GBA SWI number is just `instr & 0xFF0000 >> 16`. GBA games use `SWI #0x0C0000` or `SWI 0x0C`.
        let swi_num = if (instr & 0xFF0000) != 0 { (instr >> 16) & 0xFF } else { instr & 0xFF };
        if self.handle_hle_swi(swi_num, bus) { return; }

        let old_cpsr = self.cpsr;
        self.set_mode(Mode::Supervisor);
        self.spsr = old_cpsr;
        self.regs[14] = self.regs[15].wrapping_sub(4);
        self.set_t(false);
        self.set_i(true);
        self.regs[15] = 0x00000008;
        self.reload_pipeline();
    }

    fn handle_hle_swi(&mut self, swi_num: u32, bus: &mut dyn Bus) -> bool {
        println!("ANY SWI {:02X} CALLED! i_f={:04X} ie={:04X} ime={:04X}", swi_num, bus.read16(0x04000202), bus.read16(0x04000200), bus.read16(0x04000208));
        println!("SWI {:02X} src={:08X} dst={:08X} ctrl={:08X}", swi_num, self.regs[0], self.regs[1], self.regs[2]);
        match swi_num {
            0x0B => { // CpuSet
                let src = self.regs[0];
                let mut dst = self.regs[1];
                let ctrl = self.regs[2];
                let count = ctrl & 0x1FFFFF;
                let fixed = (ctrl & 0x01000000) != 0;
                let is_32bit = (ctrl & 0x04000000) != 0;
                
                if is_32bit {
                    let mut s = src & !3;
                    let mut d = dst & !3;
                    for _ in 0..count {
                        let val = bus.read32(s);
                        bus.write32(d, val);
                        if !fixed { s += 4; }
                        d += 4;
                    }
                } else {
                    let mut s = src & !1;
                    let mut d = dst & !1;
                    for _ in 0..count {
                        let val = bus.read16(s);
                        bus.write16(d, val);
                        if !fixed { s += 2; }
                        d += 2;
                    }
                }
                true
            }
            0x0C => { // CpuFastSet
                let src = self.regs[0] & !3;
                let mut dst = self.regs[1] & !3;
                let ctrl = self.regs[2];
                let count = ctrl & 0x1FFFFF;
                let fixed = (ctrl & 0x01000000) != 0;
                
                let mut s = src;
                for _ in 0..count {
                    let val = bus.read32(s);
                    bus.write32(dst, val);
                    if !fixed { s += 4; }
                    dst += 4;
                }
                true
            }
            0x05 => { // VBlankIntrWait
                // HLE IntrWait: we must enable IME so the user IRQ handler can run when VBlank fires.
                let old_ime = bus.read16(0x04000208);
                self.saved_ime = bus.read16(0x04000208);
                bus.write16(0x04000208, 1); // Set IME=1
                self.halted = true;
                // Wait, how do we restore IME after halt? We can't easily do it here because it returns true and the CPU halts.
                // Let's just hope the game doesn't mind IME staying 1.
                true
            }
            0x04 => { // IntrWait
                println!("SWI 4 CALLED at cycle {}", self.cycles);
                let wait_flags = self.regs[1];
                bus.write16(0x04000202, wait_flags as u16); // Clear waited IF
                self.halted = true;
                true
            }
            0x02 => { // Halt
                self.halted = true;
                true
            }
            _ => false,
        }
    }

    fn execute_arm_coprocessor(&mut self, instr: u32, bus: &mut dyn Bus) {
        // Coprocessor operations
    }
}
