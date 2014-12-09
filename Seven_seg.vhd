LIBRARY ieee ;
USE ieee.std_logic_1164.all ;
ENTITY bcd7seg IS
PORT ( bcd : IN STD_LOGIC_VECTOR(3 downto 0) ;
display : OUT STD_LOGIC_VECTOR(0 TO 6) ) ;
END bcd7seg ;
--–   ——–
--–  | 0 |
--– 5|   | 1
--–  |   |
--–   ——–
--–  | 6 |
--- 4|   | 2
--–  |   |
--–   ——–
--–    3
ARCHITECTURE seven_seg OF bcd7seg IS
BEGIN
	PROCESS ( bcd )
	BEGIN
		CASE bcd IS
			WHEN x"0" =>
				display <= "0000001" ;
			WHEN x"1" =>
				display <= "1001111" ;
			WHEN x"2" =>
				display <= "0010010" ;
			WHEN x"3" =>
				display <= "0000110" ;
			WHEN x"4" =>
				display <= "1001100" ;
			WHEN x"5" =>
				display <= "0100100" ;
			WHEN x"6" =>
				display <= "1100000" ;
			WHEN x"7" =>
				display <= "0001111" ;
			WHEN x"8" =>
				display <= "0000000" ;
			WHEN x"9" =>
				display <= "0001100" ;
			WHEN x"A" =>
				display <= "0001000" ;
			WHEN x"B" =>
				display <= "1100000" ;
			WHEN x"C" =>
				display <= "0110001" ;
			WHEN x"D" =>
				display <= "1000010" ;
			WHEN x"E" =>
				display <= "0110000" ;
			WHEN x"F" =>
				display <= "0111000" ;
			WHEN OTHERS =>
				display <= "1111111" ;
		END CASE ;
	END PROCESS ;
END seven_seg ;