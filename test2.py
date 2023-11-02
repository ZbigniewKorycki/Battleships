from board import Board
from ships_logic import Ship

board = Board()
ship = Ship("D", 3, 4, "vertical")
ship_2 = Ship("D", 3, 4, "horizontal")
board.add_ship(ship)
board.add_ship(ship_2)
# board.add_ship("D", 7, 4, "horizontal")

