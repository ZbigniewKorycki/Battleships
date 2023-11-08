import string
import random
from ships_logic import Ship, Ships
from board import Board



class Player:
    def __init__(self):
        self.ships = Ships()
        self.player_board = Board()

    def coordinates_for_ship_add_to_board(self):
        while self.ships.ships_to_deploy_list:
            try:
                for ship_type in self.ships.ships_to_deploy_list:
                    row_input = self.row_input(ship_type)
                    if row_input[0] == True:
                        row = row_input[1]
                    else:
                        print(row_input[1])
                        break
                    column_input = self.column_input(ship_type)
                    if column_input[0] == True:
                        column = column_input[1]
                    else:
                        print(column_input[1])
                        break
                    size = self.ship_size_establish(ship_type)
                    orientation_input = self.orientation_input(ship_type)
                    if orientation_input[0] == True:
                        orientation = orientation_input[1]
                    else:
                        print(orientation_input[1])
                        break
                    ship = Ship(row, column, size, orientation)
                    self.player_board.add_ship(ship)
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                print("Ship outside the board, try again")
                continue

    def row_input(self, ship_type):
        row = input(f"Set row for '{ship_type}' from 'A' to 'J': ").capitalize()
        if row in string.ascii_uppercase[:10]:
            return (True, row)
        else:
            error_message = "Row outside index"
            return (False, error_message)

    def column_input(self, ship_type):
        try:
            column = int(input(f"Set column for '{ship_type}' from '1' to '10': "))
            if column in range(1, 11):
                return (True, column)
            else:
                error_message = "Column outside index"
                return (False, error_message)
        except ValueError:
            error_message = "Column have to be an integer"
            return (False, error_message)

    def ship_size_establish(self, ship_type):
        if ship_type == "Four-masted ship":
            size = 4
        elif ship_type == "Three-masted ship":
            size = 3
        elif ship_type == "Two-masted ship":
            size = 2
        elif ship_type == "One-masted ship":
            size = 1
        return size

    def orientation_input(self, ship_type):
        if ship_type != "One-masted ship":
            orientation_input = input(f"In which direction would you set '{ship_type}' ? Put 'H' for horizontal, 'V' for vertical: ").capitalize()
            if orientation_input in ["H", "V"]:
                if orientation_input == "H":
                    orientation = "horizontal"
                elif orientation_input == "V":
                    orientation = "vertical"
                return (True, orientation)
            else:
                error_message = "Orientation have to be 'H' or 'V'"
                return (False, error_message)
        elif ship_type == "One-masted ship":
            orientation = "horizontal"
            return (True, orientation)


class AIPlayer(Player):
    def coordinates_for_ship_add_to_board(self):
            while self.ships.ships_to_deploy_list:
                try:
                    for ship_type in self.ships.ships_to_deploy_list:
                        row = self.row_input()
                        column = self.column_input()
                        size = self.ship_size_establish(ship_type)
                        orientation = self.orientation_input(ship_type)
                        ship = Ship(row, column, size, orientation)
                        self.player_board.add_ship(ship)
                        self.ships.ships_to_deploy_list.remove(ship_type)
                except KeyError:
                    continue

    def row_input(self):
        row_index = random.randint(0, 9)
        row = string.ascii_uppercase[row_index]
        return row

    def column_input(self):
        column = random.randint(1, 10)
        return column

    def orientation_input(self, ship_type):
        if ship_type != "One-masted ship":
            available_options = ["H", "V"]
            orientation = random.choice(available_options)
            if orientation == "H":
                orientation = "horizontal"
            elif orientation == "V":
                orientation = "vertical"
            return orientation
        elif ship_type == "One-masted ship":
            orientation = "horizontal"
            return orientation