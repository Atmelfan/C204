entity alu is
	generic (
		WIDTH : integer := 8
	);
	port (
		clock, carry_in: in std_logic;
		bool, carry_out: out std_logic;
		OP: in std_logic_vector(7 downto 0);
		A: in std_logic_vector(WIDTH-1 downto 0);
		B: in std_logic_vector(WIDTH-1 downto 0);
		C: out std_logic_vector(WIDTH-1 downto 0)
	);
end entity ; -- alu

architecture arch of alu is



begin



end architecture ; -- arch