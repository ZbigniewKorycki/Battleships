from player import Player, AIPlayer
from ships_logic import Ship
import string
import random


# player = Player()
# player.coordinates_for_ship_add_to_board()

aiplayer = AIPlayer()
aiplayer.coordinates_for_ship_add_to_board()
ships = aiplayer.ships.ships_coordinates_on_board
print(ships)
print(ships["Three-masted ship"], type(ships["Four-masted ship"]))
