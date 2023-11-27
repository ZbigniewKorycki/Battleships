import string
import random
from ships_logic import Ship, Ships
from board import Board, BoardAI
from custom_exception import CustomException
from data_utils import DatabaseUtils
from config_variables import db_file


class Player:
    def __init__(self):
        self.ships = Ships()
        self.player_board = Board()
        self.database_service = DatabaseUtils(db_file)

    def coords_for_ship_add_to_board(self):
        while self.ships.ships_to_deploy_list:
            try:
                for ship_type in self.ships.ships_to_deploy_list:
                    row_input = Player.row_input(ship_type)
                    if row_input[0]:
                        row = row_input[1]
                    else:
                        print(row_input[1])
                        break
                    column_input = Player.column_input(ship_type)
                    if column_input[0]:
                        column = column_input[1]
                    else:
                        print(column_input[1])
                        break
                    size = Player.ship_size_establish(ship_type)
                    orientation_input = Player.orientation_input(ship_type)
                    if orientation_input[0]:
                        orientation = orientation_input[1]
                    else:
                        print(orientation_input[1])
                        break
                    ship = Ship(row, column, size, orientation)
                    self.player_board.add_ship(ship)
                    self.player_board.draw_player_board()
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                print("Ship outside the board, try again")
                continue
            except CustomException as e:
                print(e)
                continue

    @staticmethod
    def row_input(ship_type):
        row = input(f"Set row for '{ship_type}' from 'A' to 'J': ").capitalize()
        if row in string.ascii_uppercase[:10]:
            return True, row
        else:
            error_message = "Row outside index"
            return False, error_message

    @staticmethod
    def column_input(ship_type):
        try:
            column = int(input(f"Set column for '{ship_type}' from '1' to '10': "))
            if column in range(1, 11):
                return True, column
            else:
                error_message = "Column outside index"
                return False, error_message
        except ValueError:
            error_message = "Column have to be an integer"
            return False, error_message

    @staticmethod
    def ship_size_establish(ship_type):
        if ship_type == "Four-masted ship":
            size = 4
        elif ship_type == "Three-masted ship":
            size = 3
        elif ship_type == "Two-masted ship":
            size = 2
        elif ship_type == "One-masted ship":
            size = 1
        return size

    @staticmethod
    def orientation_input(ship_type):
        if ship_type != "One-masted ship":
            orientation_input = input(
                f"In which direction would you set '{ship_type}' ? Put 'H' for horizontal, 'V' for vertical: "
            ).capitalize()
            if orientation_input in ["H", "V"]:
                if orientation_input == "H":
                    orientation = "horizontal"
                elif orientation_input == "V":
                    orientation = "vertical"
                return True, orientation
            else:
                error_message = "Orientation has to be 'H' or 'V'"
                return False, error_message
        elif ship_type == "One-masted ship":
            orientation = "horizontal"
            return True, orientation

    # for testing

    def aut_coords_for_ship_add_to_board(self):
        while self.ships.ships_to_deploy_list:
            try:
                for ship_type in self.ships.ships_to_deploy_list:
                    row = Player.aut_row_input()
                    column = Player.aut_column_input()
                    size = Player.ship_size_establish(ship_type)
                    orientation = Player.aut_orientation_input(ship_type)
                    ship = Ship(row, column, size, orientation)
                    self.player_board.add_ship(ship)
                    self.player_board.draw_player_board()
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                continue
            except CustomException:
                continue

    @staticmethod
    def aut_row_input():
        row_index = random.randint(0, 9)
        row = string.ascii_uppercase[row_index]
        return row

    @staticmethod
    def aut_column_input():
        column = random.randint(1, 10)
        return column

    @staticmethod
    def aut_orientation_input(ship_type):
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


class AIPlayer:
    def __init__(self):
        self.ships = Ships()
        self.player_board = BoardAI()
        self.database_service = DatabaseUtils(db_file)

    def coords_for_ship_add_to_board(self):
        while self.ships.ships_to_deploy_list:
            try:
                for ship_type in self.ships.ships_to_deploy_list:
                    row = AIPlayer.row_input()
                    column = AIPlayer.column_input()
                    size = Player.ship_size_establish(ship_type)
                    orientation = AIPlayer.orientation_input(ship_type)
                    ship = Ship(row, column, size, orientation)
                    self.player_board.add_ship(ship)
                    self.player_board.draw_player_board()
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                continue
            except CustomException:
                continue

    @staticmethod
    def row_input():
        row_index = random.randint(0, 9)
        row = string.ascii_uppercase[row_index]
        return row

    @staticmethod
    def column_input():
        column = random.randint(1, 10)
        return column

    @staticmethod
    def orientation_input(ship_type):
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

    def ai_shot(self):
        possible_shots = self.player_board.possible_shots
        if len(possible_shots["priority"]) > 0:
            shot = random.choice(possible_shots["priority"])
        elif len(possible_shots["normal"]) > 0:
            shot = random.choice(possible_shots["normal"])
        else:
            shot = {"row": "all possible shots used", "column": 10}
        row = shot["row"]
        column = shot["column"]
        return row, column
