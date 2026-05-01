import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

msr_mrs = """
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
"""

src = src.replace('let (op2, shift_carry) = self.get_arm_op2(instr, i_bit);', msr_mrs, 1)

with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
