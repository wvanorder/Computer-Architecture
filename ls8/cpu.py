"""CPU functionality."""

import sys

# Day one
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
# ALU Stuff 
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
DEC = 0b01100110
INC = 0b01100101
# Stack stuff
POP = 0b01000110
PUSH = 0b01000101
# Subroutine stuff
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.operations_table = {
            LDI: lambda a, b: self.reg_write(a, b),
            PRN: lambda a, b: self.reg_read(a),
            MUL: lambda a, b: self.alu('MUL', a, b),
            ADD: lambda a, b: self.alu('ADD', a, b),
            SUB: lambda a, b: self.alu('SUB', a, b),
            DIV: lambda a, b: self.alu('DIV', a, b),
            MOD: lambda a, b: self.alu('MOD', a, b),
            DEC: lambda a, b: self.alu('DEC', a, b),
            INC: lambda a, b: self.alu('INC', a, b),
            POP: lambda a, _: self.pop_stack(a),
            PUSH: lambda a, _: self.push_stack(a),
            CALL: lambda a, _: self.call(a),
            RET: lambda *_args: self.returny()
        }
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7
        

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(f"examples/{program}.ls8", "r") as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(address, v)

                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        def add(reg_a, reg_b):
            self.reg[reg_a] += self.reg[reg_b]

        def sub(reg_a, reg_b):
            self.reg[reg_a] -= self.reg[reg_b]

        def mul(reg_a, reg_b):
            self.reg[reg_a] *= self.reg[reg_b]

        def div(reg_a, reg_b):
            self.reg[reg_a] /= self.reg[reg_b]

        def mod(reg_a, reg_b):
            self.reg[reg_a] %= self.reg[reg_b]

        def inc(reg_a, _):
            self.reg[reg_a] += 1

        def dec(reg_a, _):
            self.reg[reg_a] -= 1


        math_operations = {
            "ADD": add,
            "SUB": sub,
            "MUL": mul,
            "DIV": div,
            'MOD': mod,
            "DEC": dec,
            "INC": inc
        }
        try:
            if op in math_operations :
                math_operations[op](reg_a, reg_b)
        except:    
            raise Exception("Math operation not found")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    #MAR == Memory Address Register, MDR == Memory Data Register
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def reg_write(self, register, value):
        self.reg[register] = value

    def reg_read(self, register):
        print(self.reg[register])

    def pop_stack(self, reg_address):
        self.reg[reg_address] = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def push_stack(self, reg_address):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[reg_address])

    def call(self, reg_address):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc + 2)
        self.pc = self.reg[reg_address]

    def returny(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] +=1

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.operations_table:
                self.operations_table[IR](operand_a, operand_b)
                operands = IR >> 6
                set_directly = (IR & 0b10000) >> 4
                if not set_directly:
                    self.pc += operands + 1
            elif IR == HLT:
                running = False
            else:
                print('unknown command')
                running = False