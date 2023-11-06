import string
from ships_logic import Ships


class Board:
    def __init__(self, size_rows=10, size_columns=10):
        self.size_rows = size_rows
        self.size_columns = size_columns
        self.player_board = self.create_starting_board()
        self.opponent_board = self.create_starting_board()
        self.draw_board()
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

    def draw_board(self):
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

            return self.draw_board()
        else:
            print("There`s another ship in area, or ship is not within board border try again")

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

    def check_if_ship_under_coordinate(self, row, column):
        if self.player_board[row][column] == "O":
            return False
        else:
            return True

    def check_if_coordinates_accessible_to_add_ship(self, ship_rows_list, ship_columns_list):
        for row in ship_rows_list:
            for column in ship_columns_list:
                if self.player_board[row][column] == ";":
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
        for key, value in self.row_index.items():
            if index == value:
                return key
        return False

    def verify_adding_block_to_board(self, row, column):
        if self.check_if_coordinate_within_board_border(row, column):
            self.player_board[row][column] = ";"
        else:
            print("Block outside board border.")

    def remove_blocks_from_board(self):
        for row in self.row_index:
            for column in range(1, self.size_columns + 1):
                if self.player_board[row][column] == ";":
                    self.player_board[row][column] = "~"

    def add_result_of_player_shot_to_opponent_board(self, row, column, result, sunk_ship_columns_list=None,
                                                    sunk_ship_rows_list=None):
        if self.check_if_coordinate_within_board_border(row, column):
            if result == "HIT":
                self.opponent_board[row][column] = "X"
            elif result == "MISS":
                self.opponent_board[row][column] = "M"
            elif result == "SINKING":
                for column in sunk_ship_columns_list:
                    for row in sunk_ship_rows_list:
                        self.opponent_board[row][column] = "S"
        else:
            print("Shot outside board.")


if __name__ == "__main__":
    board = Board()
