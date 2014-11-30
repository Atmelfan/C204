#Author: atmelfan
$include arch.s

init:
	ldi 1 R0
	adi 255 R0
	#sxt 1 R0
main:
	adi 1 R0
	jmp R0 R0
	+main