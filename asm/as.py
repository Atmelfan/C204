#!/usr/bin/env python 
#Author: atmelfan
import sys
import csv
import struct
import time

instructions = {
	#No operation
	"nop": 0x00,
	#Add
	"add": 0x10,
	#Subtract
	"sub": 0x20,
	#Logical and
	"and": 0x30,
	#Logical or
	"or" : 0x40,
	#Logical xor
	"xor": 0x50,
	#Copy
	"mov": 0x60,
	#Skip if equal
	"ske": 0x7,
	"rv1": 0x08,
	"rv2": 0x09,
	"rv3": 0x0A,
	"rv4": 0x0B,
	"rv5": 0x0C,
	"rv6": 0x0D,
	"rv7": 0x0E,
	"rv8": 0x0F,
	#----EXTENDED INNSTRUCTIONS----
	#Intermediate no operation
	"noi": 0x80,
	#Intermediate add
	"adi": 0x90,
	#Intermediate subtract
	"sbi": 0xA0,
	#Intermediate logcal and
	"ani": 0xB0,
	#Intermediate logical or
	"ori": 0xC0,
	#Intermediate logical xor
	"xoi": 0xD0,
	#Intermediate copy
	"ldi": 0xE0,
	#Intermediate skip if equal
	"sei": 0xF0,
	

}

symbols = {
}

def preprocess(s):
	s = s.strip().split("#")[0]
	for key in symbols:
		s = s.replace(key, "%s" % symbols[key])
	return s

def map(file, level = 0):
	word = 0
	lineno = 0
	print("\t"*level + 'Mapping "%s":' % file)
	with open(file, "r") as input:
		for line in input:
			lineno += 1
			line = line.strip().split("#")[0]
			if line.startswith("#") or len(line) == 0:
				pass
			else:
				ops = line.split()
				if ops[0].endswith(":"):
					symbol = ops[0].replace(":", "")
					symbols[symbol] = word
					print("\t"*level + 'Added label "%s" with address 0x%04x' % (symbol, word))
				elif line.startswith("$define"):
					symbols[ops[1]] = ops[2]
					try:
						print("\t"*level + 'Added symbol "%s" with value %s(0x%04x)' % (ops[1], ops[2], int(ops[2], 0)))
					except Exception, e:
						print("\t"*level + 'Added symbol "%s" with value "%s"(\033[31mwhat?\033[0m)' % (ops[1], ops[2]))
				elif line.startswith("$include"):
					print("\t"*level + 'Included "%s"' % ops[1])
					map(ops[1], level + 1)
				elif preprocess(ops[0]) in instructions:
					word += 1
					#print("%04x: %s" % (word, line))
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (ops[0], lineno))
	print("\t"*level + "Done!")

def parse_symbol(s):
	sp = s.split(":")
	val = int(sp[0], 0)
	if(len(sp) > 1):
		offset = int(sp[1], 0)
		val = (val >> offset) & 0xFF
	return val

def toword(instr, a, b):
	return (instructions[instr] << 8) | (parse_symbol(a) << 4) | parse_symbol(b)

def assemble(file):
	word = 0
	lineno = 0
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
		print("\t%-6s  %-25s  %-20s  %-6s" % ("addr", "assembly", "preprocessed", "disassembly"))
		for pre in input:
			lineno += 1
			line = preprocess(pre)
			if line.startswith("#") or line.startswith("$") or len(line) == 0:
				pass
			else:
				ops = line.split()
				if line.endswith(":"):
					pass
				elif ops[0] in instructions:
					a = ops[1] if len(ops) > 1 else "0"
					b = ops[2] if len(ops) > 2 else "0"
					dat = toword(ops[0], a, b)
					hexfile.write("%04X : %04X; --%s\n" % (word, dat, pre.strip()))
					print("\t0x%04x  %-25s  %-20s  0x%04x" % (word, pre.strip(), line, toword(ops[0], a, b)))
					word += 1
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (ops[0], lineno))	
		hexfile.write("END;")
	print("Preventing program from becoming skynet...")
	time.sleep(8)
	print("\033[31mERROR: Failed to prevent skynet!\033[0m")
	print('Saved as "%s.mif"' % file)
	print("Done!")	


print("----------GPA Robotics terrible SXT8C204 assembler----------")
map(sys.argv[1])
print("Writing symbol map to csv file...")
writer = csv.writer(open(sys.argv[1] + ".csv", 'wb'))
for key, value in symbols.items():
		writer.writerow([key, value])
assemble(sys.argv[1])
print("Bye!")