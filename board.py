import string
from ships_logic import Ships
from custom_exception import CustomException


class Board:
    def __init__(self, size_rows=10, size_columns=10):
        self.size_rows = size_rows
        self.size_columns = size_columns
        self.player_board = self.create_starting_board()
        self.opponent_board = self.create_starting_board()
        self.draw_player_board()
        self.row_index = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
            "I": 9,
            "J": 10
        }
        self.ships = Ships()

    def create_starting_board(self):
        starting_board = {
            row: {col: "~" for col in range(1, self.size_columns + 1)}
            for row in string.ascii_uppercase[0: self.size_rows]
        }
        return starting_board

    def draw_player_board(self):
        print("Player board:".center(self.size_columns * 2 + 1))
        columns = print(end="  "), [print(num, end=" ") for num in range(1, self.size_columns + 1)], print()
        rows_with_value = [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.player_board.items()
        ]

    def draw_opponent_board(self):
        print("Opponent board:".center(self.size_columns * 2 + 1))
        columns = print(end="  "), [print(num, end=" ") for num in range(1, self.size_columns + 1)], print()
        rows_with_value = [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.opponent_board.items()
        ]

    def add_ship(self, ship):
        if self.check_if_coordinates_accessible_to_add_ship(ship.rows_list, ship.columns_list):
            if ship.orientation == "horizontal":
                for column in ship.columns_list:
                    self.player_board[ship.rows_list[0]][column] = "O"
            elif ship.orientation == "vertical":
                for row in ship.rows_list:
                    self.player_board[row][ship.columns_list[0]] = "O"
            self.block_ship_near_fields(ship)
            self.ships.ships_list.append(ship)

            return self.draw_player_board()
        else:
            raise CustomException("There`s another ship in area")

    def block_ship_near_fields(self, ship):
        if ship.orientation == "horizontal":
            ship_row_index = self.row_index[ship.rows_list[0]]
            self.verify_adding_block_to_board(ship.rows_list[0], min(ship.columns_list) - 1)
            self.verify_adding_block_to_board(ship.rows_list[0], max(ship.columns_list) + 1)
            self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index - 1), min(ship.columns_list) - 1)
            self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index - 1), max(ship.columns_list) + 1)
            self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index + 1), min(ship.columns_list) - 1)
            self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index + 1), max(ship.columns_list) + 1)
            for column in ship.columns_list:
                self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index + 1), column)
                self.verify_adding_block_to_board(self.get_row_from_index(ship_row_index - 1), column)
        elif ship.orientation == "vertical":
            ship_row_indexes = [self.row_index[row] for row in ship.rows_list]
            self.verify_adding_block_to_board(self.get_row_from_index(min(ship_row_indexes) - 1), ship.columns_list[0])
            self.verify_adding_block_to_board(self.get_row_from_index(max(ship_row_indexes) + 1), ship.columns_list[0])
            self.verify_adding_block_to_board(self.get_row_from_index(min(ship_row_indexes) - 1),
                                              ship.columns_list[0] - 1)
            self.verify_adding_block_to_board(self.get_row_from_index(min(ship_row_indexes) - 1),
                                              ship.columns_list[0] + 1)
            self.verify_adding_block_to_board(self.get_row_from_index(max(ship_row_indexes) + 1),
                                              ship.columns_list[0] + 1)
            self.verify_adding_block_to_board(self.get_row_from_index(max(ship_row_indexes) + 1),
                                              ship.columns_list[0] - 1)
            for row in ship.rows_list:
                self.verify_adding_block_to_board(row, ship.columns_list[0] + 1)
                self.verify_adding_block_to_board(row, ship.columns_list[0] - 1)

    def check_if_coordinates_accessible_to_add_ship(self, ship_rows_list, ship_columns_list):
        for row in ship_rows_list:
            for column in ship_columns_list:
                if self.player_board[row][column] == ";" or self.player_board[row][column] == "O":
                    return False
                if not self.check_if_coordinate_within_board_border(row, column):
                    return False
        else:
            return True

    def check_if_coordinate_within_board_border(self, row, column):
        if row in self.row_index and column in range(1, self.size_columns + 1):
            return True
        else:
            return False

    def get_row_from_index(self, index):
        for row, value in self.row_index.items():
            if index == value:
                return row
        return None

    def verify_adding_block_to_board(self, row, column):
        if self.check_if_coordinate_within_board_border(row, column):
            self.player_board[row][column] = ";"
        # else:
        #     print("Block outside board border.")

    def remove_blocks_from_board(self):
        for row in self.row_index:
            for column in range(1, self.size_columns + 1):
                if self.player_board[row][column] == ";":
                    self.player_board[row][column] = "~"

    def add_result_of_player_shot_into_opponent_board(self, row, column, result):
        if self.check_if_coordinate_within_board_border(row, column):
            if result == "HIT":
                self.opponent_board[row][column] = "X"
            elif result == "MISS":
                self.opponent_board[row][column] = "M"
            elif result == "SINKING":
                coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(row, column)
                print(coordinates_of_sunk_ship)
                for coordinate in coordinates_of_sunk_ship:
                    self.opponent_board[coordinate["row"]][coordinate["column"]] = "S"
        else:
            print("Shot outside board.")

    def result_of_opponent_shot(self, row, column):
        if self.check_if_coordinate_within_board_border(row, column):
            if self.player_board[row][column] == "O":
                hit_ship = self.get_ship_by_coordinate(row, column)
                if hit_ship.ship_hit() == 0:
                    result = "SINKING"
                    self.mark_opponent_shot_result_into_player_board(row, column, result)
                    return result
                else:
                    result = "HIT"
                    self.mark_opponent_shot_result_into_player_board(row, column, result)
                    return result
            elif self.player_board[row][column] == "~" or self.player_board[row][column] == "X" or self.player_board[row][column] == ";":
                result = "MISS"
                self.mark_opponent_shot_result_into_player_board(row, column, result)
                return result
        else:
            return "The shot is not within the boundaries of the board."

    def get_ship_by_coordinate(self, row, column):
        for ship in self.ships.ships_list:
            if row in ship.rows_list and column in ship.columns_list:
                return ship

    def mark_opponent_shot_result_into_player_board(self, row, column, result):
        if result == "MISS":
            self.player_board[row][column] = "M"
        elif result == "HIT":
            self.player_board[row][column] = "X"
        elif result == "SINKING":
            sunk_ship = self.get_ship_by_coordinate(row, column)
            for column in sunk_ship.columns_list:
                for row in sunk_ship.rows_list:
                    self.player_board[row][column] = "S"

    def prepare_board_for_game_start(self):
        self.remove_blocks_from_board()
        self.draw_player_board()
        self.draw_opponent_board()

    def get_coordinates_of_sunk_ship_from_last_hit_coordinate(self, row, column):
        ship_row_index = self.row_index[row]
        coordinates_of_sunk_ship = [{"row": row, "column": column}]
        direct_neighboring_coordinates = [
            [[ship_row_index, column - 1], [ship_row_index, column - 2], [ship_row_index, column - 3]], #left
            [[ship_row_index, column + 1], [ship_row_index, column + 2], [ship_row_index, column + 3]], #right
            [[ship_row_index - 1, column], [ship_row_index - 2, column], [ship_row_index - 3, column]], #up
            [[ship_row_index + 1, column], [ship_row_index + 2, column], [ship_row_index + 3, column]]] #down
        for direction in direct_neighboring_coordinates:
            for distance_apart_ship in direction:
                neighboring_row_index, neighboring_column = distance_apart_ship
                neighboring_row = self.get_row_from_index(neighboring_row_index)
                if self.check_if_coordinate_within_board_border(neighboring_row, neighboring_column):
                    if self.opponent_board[neighboring_row][neighboring_column] == "X":
                        coordinates_of_sunk_ship.append({"row": neighboring_row,
                                                         "column": neighboring_column})
                    else:
                        break
        return coordinates_of_sunk_ship

    def get_positions_of_all_ships(self):
        return self.ships.ships_coordinates_on_board


if __name__ == "__main__":
    board = Board()
