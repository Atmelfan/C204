library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity fetchy is
	port(
		clk, skip: in std_logic; 
		data: in std_logic_vector(15 downto 0);
		addr: out std_logic_vector(11 downto 0);
		instr: out std_logic_vector(15 downto 0)
	);
end fetchy;

architecture arch of fetchy is
	signal pc: std_logic_vector(11 downto 0) := "000000000000";
begin
	
	process(clk, pc, data, skip) 
	begin
		if(rising_edge(clk)) then
			if(data(15 downto 12) = x"F") then
				pc <= data(11 downto 0);
			else
				if(skip = '1') then
					pc <= pc + 2;
				else
					pc <= pc + 1;
				end if;
			end if;
		end if;
	end process;
	addr <= pc;
	instr <= data;

end architecture;