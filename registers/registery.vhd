library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity registery is
	generic (
		WIDTH: integer := 8;
		PROG: integer := 16
	);
	port (
		--Register input/outputs
		clock, wren: in std_logic;
		addr_A, addr_B: in integer range 0 to 15;
		read_A, read_B: out std_logic_vector(WIDTH-1 downto 0);
		write_B: in std_logic_vector(WIDTH-1 downto 0);
		--
		leds: out std_logic_vector(WIDTH-1 downto 0); 
		--Program counter output
		skip: in std_logic;
		pcout: out std_logic_vector(PROG-1 downto 0);
		--External memory output
		wr: inout std_logic;
		data: inout std_logic_vector(WIDTH-1 downto 0);
		addr: inout std_logic_vector(15 downto 0)
	);
end entity ; -- alu

architecture arch of registery is
	type mem is array(0 to 14) of std_logic_vector(WIDTH-1 downto 0);
	signal registers: mem;
	signal pc: std_logic_vector(PROG-1 downto 0) := (others => '0');
begin
	--Asynchronous read from registers or databuss
	--A read port
	process(addr_A, data, pc, registers)
	begin
		case addr_A is
			when 15 => read_A <= data;
			when 12 => read_A <= pc(15 downto 8);
			when 11 => read_A <= pc( 7 downto 0);
			when others => read_A <= registers(addr_A);
		end case;
	end process;
	--B read port
	process(addr_B, data, pc, registers)
	begin
		case addr_B is
			when 15 => read_B <= data;
			when 12 => read_B <= pc(15 downto 8);
			when 11 => read_B <= pc( 7 downto 0);
			when others => read_B <= registers(addr_B);
		end case;
	end process;
	
	--Synchronous write on falling edge
	process(clock, wren, registers, skip)
	begin
		--On falling edge, write data to registers or databuss
		if(falling_edge(clock)) then
			--If writing to PCH register, update PC
			if(addr_B = 12  and wren = '1') then
				pc <= write_B&registers(11);
				registers(addr_B) <= write_B;
			--If not, increment PC as normal and write to registers
			else
				if(skip = '1') then
					pc <= pc + 2;
				else
					pc <= pc + 1;
				end if;
				--If writing to DAT, write to databus instead
				if(addr_B = 15 and wren = '1') then
					data <= write_B;
				--If writing to PCL DO NOT UPDATE REGISTERS
				elsif(addr_B = 11  and wren = '1') then
					registers(addr_B) <= write_B;
				--Not working with PCL or PCH, update them (and write to whatever register selected)
				elsif(wren = '1') then
					registers(11) <= pc( 7 downto 0);
					registers(12) <= pc(15 downto 8);
					registers(addr_B) <= write_B;
				end if;
			end if;
		end if;
	end process;
	
	--If reading/writing to register 15(DAT) set address so to external memory, else let them float.
	addr <= registers(13)&registers(14) when addr_A = 15 or addr_B = 15 else (others => 'Z');
	wr <= '0' when addr_A = 15 or addr_B = 15 else 'Z';
	pcout <= pc;
	leds <= registers(0);

end architecture ; -- arch