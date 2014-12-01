library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity alu is
	generic (
		WIDTH : integer := 8
	);
	port (
		wr, skip: out std_logic;
		OP: in std_logic_vector(3 downto 0);
		A: in std_logic_vector(WIDTH-1 downto 0);
		B: in std_logic_vector(WIDTH-1 downto 0);
		C: out std_logic_vector(WIDTH-1 downto 0)
	);
end entity ; -- alu

architecture arch of alu is
begin

process(OP, A, B)
begin
	case OP is
		--0x0, NOP
		when x"0" =>
			wr <= '0';
			skip <= '0';
			C <= (others => '0');
		--0x1, ADD
	   when x"1" =>
			wr <= '1';
			skip <= '0';
			C <= B + A;
		--0x2, SUB
		when x"2" =>
			wr <= '1';
			skip <= '0';
			C <= B - A;
		--0x3, AND
		when x"3" =>
		   wr <= '1';
			skip <= '0';
			C <= B and A;
		--0x4, OR
		when x"4" =>
			wr <= '1';
			skip <= '0';
			C <= B or A;
		--0x5, XOR
		when x"5" =>
			wr <= '1';
			skip <= '0';
			C <= B xor A;
		--0x6, MICKE
		when x"6" =>
			wr <= '1';
			skip <= '0';
			C <= A;
		--0x7, skne
		when x"7" =>
			wr <= '0';
			if(A = B) then
				skip <= '1';
			else
				skip <= '0';
			end if;
			C <= (others => '0');
		when others =>
			wr <= '0';
			skip <= '0';
			C <= (others => '0');
	end case;
end process;

end architecture ; -- arch