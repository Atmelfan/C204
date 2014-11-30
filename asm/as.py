#!/usr/bin/env python 
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
	"reset": 0x0000
}

program = [0x0000]

def map(file):
	word = 0
	lineno = 0
	with open(file, "r") as input:
		for line in input:
			lineno += 1
			line = line.strip()
			if line.startswith("#") or len(line) == 0:
				pass
			else:
				first = line.split()[0]
				if first.endswith(":"):
					symbol = first.replace(":", "")
					symbols[symbol] = word
					print("Added symbol '%s' as 0x%04x" % (symbol, word))
				elif first in instructions or first.startswith("+"):
					word += 1
				else:
					raise Exception("Unknown instruction: '%s' at line %s" % (first, lineno))
	print("Writing symbol map to csv file...")
	writer = csv.writer(open(file + ".csv", 'wb'))
	for key, value in symbols.items():
   		writer.writerow([key, value])	

def toword(instr, a, b):
	for key in symbols:
		instr = instr.replace(key, "0x%04x" % symbols[key])
		a = a.replace(key, "0x%04x" % symbols[key])
		b = b.replace(key, "0x%04x" % symbols[key])
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
			if line.startswith("#") or len(line) == 0:
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
assemble(sys.argv[1])