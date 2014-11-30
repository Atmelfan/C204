#!/usr/bin/env python 
#Author: atmelfan
import sys
import csv
from intelhex import IntelHex

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
	"jmi": 0xF
}

symbols = {
}

program = [0x0000]

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
						print("\t"*level + "Added symbol '%s' with value %s(what?)" % (ops[1], ops[2]))
				elif line.startswith("$include"):
					print("\t"*level + "Included %s" % ops[1])
					map(ops[1], level + 1)
				elif ops[0] in instructions or ops[0].startswith("+"):
					word += 1
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (ops[0], lineno))
	print("\t"*level + "done!")
		

def toword(instr, a, b):
	for key in symbols:
		instr = instr.replace(key, "%s" % symbols[key])
		a = a.replace(key, "%s" % symbols[key])
		b = b.replace(key, "%s" % symbols[key])
	if instr.startswith("+"):
		return int(instr[1:], 0)
	else:
		return (instructions[instr] << 12) | (int(a, 0) << 4) | int(b, 0)

def assemble(file):
	ih = IntelHex()
	word = 0
	with open(file, "r") as input, open(file + ".hex", "wb") as hexfile:
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
					ih[word+1] = ((dat & 0x00FF) >> 0)
					ih[word+0] = ((dat & 0xFF00) >> 8)
					print("%s > 0x%04x" % (ops[0], toword(ops[0], ops[1], ops[2])))
					word += 2
				elif ops[0].startswith("+"):
					dat = toword(ops[0], "", "")
					ih[word+1] = ((dat & 0x00FF) >> 0)
					ih[word+0] = ((dat & 0xFF00) >> 8)
					print("%s > 0x%04x" % (ops[0], toword(ops[0], "", "")))
					word += 2
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (first, lineno))		
		print("Writing program to hex file...")
		ih.tofile(hexfile, format='hex')


map(sys.argv[1])
print("Writing symbol map to csv file...")
writer = csv.writer(open(sys.argv[1] + ".csv", 'wb'))
for key, value in symbols.items():
		writer.writerow([key, value])
assemble(sys.argv[1])