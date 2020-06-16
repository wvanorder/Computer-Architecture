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

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.operations_table = {
            LDI: lambda a, b: self.reg_write(a, b),
            PRN: lambda a, b: self.ram_read(a),
            MUL: lambda a, b: self.alu('MUL', a, b)
        }
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        

    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(f"examples/{program}.ls8", "r") as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 10)
                except ValueError:
                    continue
                self.ram_write(address, v)

                address += 1



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR in self.operations_table:
                print('command found')
                self.operations_table[IR](operand_a, operand_b)
                operands = IR >> 6
                set_directly = (IR & 0b10000) >> 4
                if not set_directly:
                    self.pc += operands + 1
            elif IR == HLT:
                running = False
            else:
                print(IR)
                print('unknown command')
                running = False