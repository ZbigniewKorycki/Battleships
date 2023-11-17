import string
import random
import time
from ships_logic import Ship, Ships
from board import Board
from custom_exception import CustomException
from data_utils import Database
from config_variables import db_file


class Player:
    def __init__(self):
        self.ships = Ships()
        self.player_board = Board()
        self.database_service = Database(db_file)

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
                    self.ships.save_ships_coordinates(ship_type, ship)
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                print("Ship outside the board, try again")
                continue
            except CustomException as e:
                print(e)
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
            orientation_input = input(
                f"In which direction would you set '{ship_type}' ? Put 'H' for horizontal, 'V' for vertical: ").capitalize()
            if orientation_input in ["H", "V"]:
                if orientation_input == "H":
                    orientation = "horizontal"
                elif orientation_input == "V":
                    orientation = "vertical"
                return (True, orientation)
            else:
                error_message = "Orientation has to be 'H' or 'V'"
                return (False, error_message)
        elif ship_type == "One-masted ship":
            orientation = "horizontal"
            return (True, orientation)

    def show_boards_status_for_archived_game(self):
        all_games = self.database_service.show_all_games()
        for game in all_games:
            print(game)
        try:
            game_number = input("Which game you want to see ?: ")
            if int(game_number) > len(all_games):
                print("There`s no game with this ID number.")
            else:
                game_id = int(game_number)
                boards = self.database_service.show_board_status_for_game(game_id)
                time_in_sec = input("How fast you want to watch this game ? (type seconds between next boards): ")
                int_time_in_sec = int(time_in_sec)
                for board in boards:
                    print(board)
                    time.sleep(int_time_in_sec)
        except ValueError:
            print(f"Game number has to be an integer in range: {len(all_games)} / Type time in seconds.")


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
                    self.ships.save_ships_coordinates(ship_type, ship)
                    self.ships.ships_to_deploy_list.remove(ship_type)
            except KeyError:
                continue
            except CustomException:
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

    def ai_shot(self):
        possible_shots = self.player_board.possible_shots_for_ai
        if len(possible_shots["priority"]) > 0:
            shot = random.choice(possible_shots["priority"])
        else:
            shot = random.choice(possible_shots["normal"])
        row = shot["row"]
        column = shot["column"]
        return row, column
