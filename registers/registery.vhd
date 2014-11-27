library ieee;
use ieee.std_logic_1164.all;

entity registery is
	generic (
		WIDTH: integer := 8
	);
	port (
		clock, wren: in std_logic;
		addr_A, addr_B: in integer range 0 to 15;
		read_A, read_B: out std_logic_vector(WIDTH-1 downto 0);
		write_B: in std_logic_vector(WIDTH-1 downto 0)
	);
end entity ; -- alu

architecture arch of registery is
	type mem is array(0 to 15) of std_logic_vector(WIDTH-1 downto 0);
	signal registers: mem;
begin
	--Asynchronous read
	read_A <= registers(addr_A);
	read_B <= registers(addr_B);
	--Synchronous write on falling edge
	process(clock, wren)
	begin
		if(falling_edge(clock) and wren = '1') then
			registers(addr_B) <= write_B;
		end if;
	end process;

end architecture ; -- arch