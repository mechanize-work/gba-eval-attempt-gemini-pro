import sys

with open("src/cpu/arm7tdmi.rs", "r") as f:
    src = f.read()

# Add cycles to thumb push/pop
src = src.replace('        if l_bit { // POP\n            let mut addr = self.regs[13];',
                  '        if l_bit { // POP\n            let mut addr = self.regs[13];\n            let num_regs = r_list.count_ones() + if r_bit { 1 } else { 0 };\n            self.cycles += self.get_memory_cycles_32(addr) * (num_regs as usize);')

src = src.replace('        } else { // PUSH\n            let num_regs = r_list.count_ones() + if r_bit { 1 } else { 0 };',
                  '        } else { // PUSH\n            let num_regs = r_list.count_ones() + if r_bit { 1 } else { 0 };\n            self.cycles += self.get_memory_cycles_32(self.regs[13]) * (num_regs as usize);')

# Add cycles to thumb multiple load/store
src = src.replace('let num_regs = if r_list == 0 { 0 } else { r_list.count_ones() };\n        \n        let start_addr = addr;',
                  'let num_regs = if r_list == 0 { 0 } else { r_list.count_ones() };\n        self.cycles += self.get_memory_cycles_32(addr) * (num_regs as usize);\n        let start_addr = addr;')
src = src.replace('let mut addr = self.regs[rb];\n\n        for i in 0..8 {',
                  'let mut addr = self.regs[rb];\n        let num_regs = if r_list == 0 { 0 } else { r_list.count_ones() };\n        self.cycles += self.get_memory_cycles_32(addr) * (num_regs as usize);\n        for i in 0..8 {')


# Add cycles to ARM LDM/STM
src = src.replace('let mut addr = self.regs[rn];\n        let num_regs = reg_list.count_ones();',
                  'let mut addr = self.regs[rn];\n        let num_regs = reg_list.count_ones();\n        self.cycles += self.get_memory_cycles_32(addr) * (num_regs as usize);')


with open("src/cpu/arm7tdmi.rs", "w") as f:
    f.write(src)
