import re

'''
Write your hmmm file following these rules:
    1) Instead of writing line numbers, write "NN". The compiler will see these and replace them with the appropriate number
    2) Under specific circumstances, if you program needs to jump from one address to another, write that address as "@whatever you want@" specific address names should be enclosed by the 'at' "@" symbol. Make sure to use this on the line being jumped to as well.
    3) Instead of writing "r1" or "r15", write "$whatever you want$" register names should be enclosed by the dollar "$" symbol
    4) There is one built in specific address: "@END@" this will always be set to the address immediately after the end of the code region. Trying to use this as a line number will be problematic, only use it as a reference.

Example program syntax based on the online HMMM Simulator factorial example

NN  read  $N$                                       # Get N
NN  setn  $PRODUCT_SO_FAR$ 1
@ITERATION_START@  jeqzn $N$ @QUIT_AND_WRITE@       # Quit if N has reached zero
NN  mul   $PRODUCT_SO_FAR$ $N$ $PRODUCT_SO_FAR$     # Update product
NN  addn  $N$ -1                                    # Decrement N
NN  jumpn @ITERATION_START@                         # Back for more

@QUIT_AND_WRITE@  write  r2
NN  halt
'''

def compile_hmmm(filename):

    if filename[-16:] == "_uncompiled.hmmm":
        pass
    else:
        print("only pass files named '()...)_uncompiled.hmmm' to this function!")
        print(f"your file ending was: '{filename[-16:]}'")
        return None

    lines = open(filename, 'r').readlines()
    edited_lines = []

    addresses = {}
    registers = {}

    line_count = 0
    register_count = 1

    for line in lines:
        if re.match("^NN", line):
            line = re.sub("^NN", f"{line_count:03}", line)
            line_count += 1

        temp_addresses = re.findall(r"^@.*?@", line)
        if len(temp_addresses) > 0:
            for addr in temp_addresses:
                if addr in addresses:
                    pass
                else:
                    addresses[addr] = f"{line_count:03}"
                    line_count += 1
        
        temp_registers = re.findall("\$.*?\$", line)
        if len(temp_registers) > 0:
            for reg in temp_registers:
                if reg in registers:
                    pass
                else:
                    registers[reg] = f"r{register_count}"
                    register_count += 1

        edited_lines.append(line)

    new_text = "".join(edited_lines)

    addresses["@END@"] = f"{line_count:03}"

    for addr in addresses:
        new_text = re.sub(addr, addresses[addr], new_text)
    for reg in registers:
        new_text = re.sub(f"\${reg[1:-1]}\$", registers[reg], new_text)

    new_file = open(f"{filename[:-16]}.hmmm", 'w')
    new_file.write(new_text)



