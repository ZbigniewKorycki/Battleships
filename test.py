from board import Board
from ships_logic import Ship
import string

board = Board()
ship = Ship("A", 1, 4, "horizontal")
ship_2 = Ship("C", 8, 3, "horizontal")
ship_3 = Ship("H", 4, 2, "vertical")
ship_4 = Ship("G", 5, 3, "vertical")
# # board.add_ship(ship)
# # board.add_ship(ship_2)
# # board.add_ship(ship_3)
# # board.add_ship(ship_4)
#

# print(ship_2)
print(ship_3)
print(ship_4)
print(ship_3.rows_list, ship_3.columns_list)
print(ship_4.rows_list, ship_4.columns_list)
