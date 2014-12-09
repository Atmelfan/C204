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

 --operation
	op: out std_logic_vector(3 downto 0);
	
 --fetchy should ignore next word
	extended: out std_logic
	
 );
end decodey;

architecture arch of decodey is
begin

	Asel <= ins(7 downto 4);
	Bsel <= ins(3 downto 0);
	Inter <= ins(11 downto 4);
	op <= "0" & ins(14 downto 12);
	muxsel <= ins(15);
	
	extended <= '1' when ins(15 downto 12) = "-111" else '0';
	


end arch;