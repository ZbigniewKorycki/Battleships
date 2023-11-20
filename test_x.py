from board import Board
from ships_logic import Ship

board = Board()
ship_11 = Ship("A", 1, 1, "horizontal")
ship_12 = Ship("C", 1, 1, "horizontal")
ship_13 = Ship("E", 1, 1, "horizontal")
ship_14 = Ship("G", 1, 1, "horizontal")
ship_21 = Ship("I", 1, 2, "vertical")
ship_22 = Ship("A", 3, 2, "horizontal")
ship_23 = Ship("A", 8, 2, "horizontal")
ship_31 = Ship("C", 5, 3, "horizontal")
ship_32 = Ship("E", 5, 3, "horizontal")
ship_41 = Ship("H", 5, 4, "horizontal")

print(ship_41.coordinates)
print(ship_31.coordinates)
print(ship_21.coordinates)
print(ship_11.coordinates)



board.add_ship(ship_11)
board.add_ship(ship_12)
board.add_ship(ship_13)
board.add_ship(ship_14)
board.add_ship(ship_21)
board.add_ship(ship_22)
board.add_ship(ship_23)
board.add_ship(ship_31)
board.add_ship(ship_32)
board.add_ship(ship_41)

board.prepare_board_for_game_start()

board.draw_player_board()

print(board.ships.get_ships_coordinates_on_board())



