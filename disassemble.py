# EVM Bytecode Dissassembler
# Author: Zach Lafeer
# Usage: python3 dissassemble.py input output

import sys
from opcodes import hex_to_opcode

# Formatted Print
def display(address, value, condition):
    if not condition:
        return
    print("0x{:X}\t".format(address), value)

# Open Files
src_file = open(sys.argv[1]).read()
out_file = open(sys.argv[2], "w")

# Redirect Stdout
original_stdout = sys.stdout
sys.stdout = out_file

# Split Bytecode into Bytes
bytes = [src_file[i:i+2].upper() for i in range(0, len(src_file), 2)]

# Byte Offset
byte = 0

# Offset in Deployed Contract
address = 0

# Bytes in Immediate Operand
immediate = 0

# True when Reached Deployed Code
deployed = False

# Iterate through bytecode
while byte < len(bytes):

    # Extract Immediate Operand
    if immediate > 0:
        value = "0x" + "".join(bytes[byte:byte+immediate])
        display(address, value, deployed)
        byte += immediate
        address += immediate
        immediate = 0
    
    # Translate to Opcode
    else:
        opcode = hex_to_opcode(bytes[byte])
        display(address, opcode, deployed)
        byte += 1
        address += 1

        # PUSH requires Immediate Operand
        if opcode[:4] == "PUSH":
            immediate = int(opcode[4:])

        # Deployment Code ends with INVALID
        elif deployed == False and opcode == "INVALID":
            deployed = True
            address = 0

# Restore Stdout
sys.stdout = original_stdout

# Close Output File
out_file.close()
