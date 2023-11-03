from board import Board
from ships_logic import Ship
import string

board = Board()
ship = Ship("A", 1, 4, "horizontal")
ship_2 = Ship("A", 8, 3, "horizontal")
ship_3 = Ship("F", 4, 2, "vertical")
ship_4 = Ship("G", 5, 3, "vertical")
board.add_ship(ship)
board.add_ship(ship_2)
board.add_ship(ship_3)
board.add_ship(ship_4)
#
# print(ship.ship_coordinates())
# print(ship_2.ship_coordinates())
# print(ship_3.ship_coordinates())
# print(ship_4.ship_coordinates())

