from board import Board
from ships_logic import Ship

board = Board()
ship = Ship("B", 5, 3, "vertical")
ship_2 = Ship("D", 1, 2, "horizontal")
# board.add_ship("A", 5, 3, "horizontal")
board.add_ship(ship)
board.add_ship(ship_2)
# board.add_ship("D", 7, 4, "horizontal")
print(board.ships.ships_list)
