#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

programs = {'call', 'interrupts', 'keyboard', 'mult', 'print8', 'printstr', 'sctest', 'stack', 'stackoverflow'}

try:
    program = sys.argv[1]
    if program in programs:
        cpu.load(program)
        cpu.run()
    else:
        print('Tha program does not exist... yet!')
except IndexError:
    print('You must put in a program name')