library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity fetchy is
	port(
		clk, extended, jmp_en: in std_logic; 
		data: in std_logic_vector(15 downto 0);
		addr: out std_logic_vector(11 downto 0);
		instr: out std_logic_vector(15 downto 0)
	);
end fetchy;

architecture arch of fetchy is
	signal pc: std_logic_vector(11 downto 0) := "000000000000";
begin
	
	process(clk, pc, extended, data, jmp_en) 
	begin
		if(rising_edge(clk)) then
			if(data(15 downto 12) = x"F") then
				pc <= data(11 downto 0);
			else
				pc <= pc + 1;
			end if;
		end if;
	end process;
	addr <= pc;
	instr <= data;

end architecture;