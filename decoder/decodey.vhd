library ieee;
use ieee.std_logic_1164.all;

entity decodey is
	port(
--INSTRUCTIONz
	ins: in std_logic_vector(15 downto 0);
	
 --select registrery
	Asel: out std_logic_vector(3 downto 0);
	Bsel: out std_logic_vector(3 downto 0);
	muxsel: out std_logic; -- selects between A register and intermediate.
	
 --Intermediate
	Inter: out std_logic_vector(7 downto 0);

<<<<<<< HEAD
 --operation
	op: out std_logic_vector(3 downto 0);
	
 --fetchy should ignore next word
	extended: out std_logic
=======
	--operation
	op: out std_logic_vector(3 downto 0)
>>>>>>> origin/master
	
 );
end decodey;

architecture arch of decodey is
begin
	--iccc_eeee_aaaa_bbbb
	--c = op code
	--e = extended op code or upper 4bit intermediate data if i=1
	--a = A operand or lower 4bit intermediate if i=1
	--b = B operand 
	Asel <= ins(7 downto 4);
	Bsel <= ins(3 downto 0);
	Inter <= ins(11 downto 4);
	--If op = "0000" => op = eeee else op = 0ccc
	op <= ins(11 downto 8) when ins(15 downto 12) = "0000" else "0"&ins(14 downto 12) ;
	
	muxsel <= ins(15);
end arch;