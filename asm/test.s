#Author: atmelfan
$include arch.s

#init
init:
	#Kopiera 1 till register 0
	ldi 1 R0
	ldi 1 R1
	ldi 2 R2
	ldi 3 R3
	ldi 4 R4
	ldi 5 R5
	ldi 6 R6
	ldi 7 R7
	ldi 8 R8
	ldi 9 R9
	ldi 10 R10
	ldi 11 R12
	ldi 12 R12
	ldi 13 R13
	ldi 14 R14
	ldi 0xFF R15

#main
main:
	#Addera 1 till register 0
	add R0 R1
	#till main
	+main
