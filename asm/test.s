#Author: atmelfan
$include arch.s

#init
init:
	#Kopiera 1 till register 0
	micke 1 R0
	#Addera 255 till register 0
	adi 255 R0
#main

main:
	#Addera 1 till register 0
	adi 1 R0
	#Hoppa
	jmp R0 R0
	#till main
	+main