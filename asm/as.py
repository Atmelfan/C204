#!/usr/bin/env python 
#Author: atmelfan
import sys
import csv
import struct
import time

instructions = {
	"nop": 0x0,
	"add": 0x1,
	"sub": 0x2,
	"and": 0x3,
	"or" : 0x4,
	"xor": 0x5,
	"mov": 0x6,
	"jmp": 0x7,
	"noi": 0x8,
	"adi": 0x9,
	"sbi": 0xA,
	"ani": 0xB,
	"ori": 0xC,
	"xoi": 0xD,
	"ldi": 0xE,
	"micke": 0xE,
}

symbols = {
}

def map(file, level = 0):
	word = 0
	lineno = 0
	print("\t"*level + "Mapping %s:" % file)
	with open(file, "r") as input:
		for line in input:
			lineno += 1
			line = line.strip()
			if line.startswith("#") or len(line) == 0:
				pass
			else:
				ops = line.split()
				if ops[0].endswith(":"):
					symbol = ops[0].replace(":", "")
					symbols[symbol] = word
					print("\t"*level + "Added label '%s' with address 0x%04x" % (symbol, word))
				elif line.startswith("$define"):
					symbols[ops[1]] = ops[2]
					try:
						print("\t"*level + "Added symbol '%s' with value %s(0x%04x)" % (ops[1], ops[2], int(ops[2], 0)))
					except Exception, e:
						print("\t"*level + "Added symbol '%s' with value %s(\033[31mwhat?\033[0m)" % (ops[1], ops[2]))
				elif line.startswith("$include"):
					print("\t"*level + "Included %s" % ops[1])
					map(ops[1], level + 1)
				elif ops[0] in instructions or ops[0].startswith("+"):
					word += 1
					#print("%04x: %s" % (word, line))
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (ops[0], lineno))
	print("\t"*level + "Done!")
		

def toword(instr, a, b):
	for key in symbols:
		instr = instr.replace(key, "%s" % symbols[key])
		a = a.replace(key, "%s" % symbols[key])
		b = b.replace(key, "%s" % symbols[key])
	if instr.startswith("+"):
		return 0xF000 | int(instr[1:], 0)
	else:
		return (instructions[instr] << 12) | (int(a, 0) << 4) | int(b, 0)

def assemble(file):
	word = 0
	print("Assembling %s:" % file)
	with open(file, "r") as input, open(file + ".mif", "w") as hexfile:
		hexfile.write("""
--                  #
--                # #  #                 #########   ##########    #########
--              # # #  # #              ###     ###  ##      ###  ###     ###
--            # # # #  # # #            ##           ##       ##  ##       ##
--          # # # # #  # # # #          ##           ###     ###  ##       ##
--        # # # # # #  # # # # #        ##   ######  ##########   ###########
--      # # # # # #    # # # # # #      ##       ##  ##           ##       ##
--    # # # # # #        # # # # # #    ###     ###  ##           ##       ##
--                          # # # # # #   #########   ##           ##       ##
--  # # # # # #                       
--    # # # # # #        # # # # # #    ##########    #########   ##########    #########   ########  ####   #########    #########
--      # # # # # #    # # # # # #      ##      ###  ###     ###  ##       ##  ###     ###     ##      ##   ###     ###  ###     ###
--        # # # # #  # # # # # #        ##       ##  ##       ##  ##       ##  ##       ##     ##      ##   ##           ##
--          # # # #  # # # # #          ##      ###  ##       ##  ##########   ##       ##     ##      ##   ##            #####
--            # # #  # # # #            ##########   ##       ##  ##       ##  ##       ##     ##      ##   ##                 ####
--              # #  # # #              ##      ###  ##       ##  ##       ##  ##       ##     ##      ##   ##                    ##
--                #  # #                ##       ##  ###     ###  ##       ##  ###     ###     ##      ##   ###     ###  ###     ###
--                   #                  ##       ##   #########   ##########    #########      ##     ####   #########    #########
-- UNNECESSARILY LARGE LOGO!
DEPTH = 4096;
WIDTH = 16;
ADDRESS_RADIX = HEX;
DATA_RADIX = HEX;
CONTENT
BEGIN\n""")
		print("\033[31mERROR: UNNECESSARILY LARGE LOGO is too small!\033[0m")
		time.sleep(5)
		for line in input:
			line = line.strip()
			if line.startswith("#") or line.startswith("$") or len(line) == 0:
				pass
			else:
				ops = line.split()
				if line.endswith(":"):
					pass
				elif ops[0] in instructions:
					dat = toword(ops[0], ops[1], ops[2])
					hexfile.write("%04X : %04X; --%s\n" % (word, dat, line))
					print("\t0x%04x %s -> 0x%04x" % (word, line, toword(ops[0], ops[1], ops[2])))
					word += 1
				elif ops[0].startswith("+"):
					dat = toword(ops[0], "", "")
					hexfile.write("%04X : %04X; --%s\n" % (word, dat, line))
					print("\t0x%04x %s -> 0x%04x" % (word, line, toword(ops[0], "", "")))
					word += 1
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (first, lineno))	
		hexfile.write("END;")
		print("Preventing program from becomming skynet...")
		time.sleep(4)
		print("\033[31mERROR: Failed to prevent skynet!\033[0m")
		print('Saving as "%s.mif"' % file)
		time.sleep(2)
		print("Done!")	


print("----------GPA Robotics terrible SXT8C204 assembler----------")
time.sleep(2)
map(sys.argv[1])
print("Writing symbol map to csv file...")
writer = csv.writer(open(sys.argv[1] + ".csv", 'wb'))
for key, value in symbols.items():
		writer.writerow([key, value])
assemble(sys.argv[1])
print("\033[31mERROR: Failed to find the ultimate question to life, the universe and everything!\033[0m")
print("Bye!")