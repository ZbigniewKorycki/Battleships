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

    def count_sunk_signs(self):
        numbers_of_sunk_signs = sum(
            [1 for key_outer, inner_dict in self.opponent_board.items() for key_inner, value in inner_dict.items() if
             value == "S"])
        return numbers_of_sunk_signs

    def add_ship(self, ship):
        if self.check_if_coordinates_accessible_to_add_ship(ship.coordinates):
            for coordinate in ship.coordinates:
                self.update_player_board(coordinate, "O")
            self.block_coordinates_near_ship(ship.coordinates)
            self.ships.active_ships.append(ship)
            return True
        else:
            raise CustomException("There`s another ship in area")

    def block_coordinates_near_ship(self, coordinates):
        for coordinate in coordinates:
            neighboring_coordinates = self.get_neighboring_coordinates_in_eight_directions(coordinate)
            for neighboring_coordinate in neighboring_coordinates:
                if neighboring_coordinate not in coordinates and self.get_symbol_from_player_board(
                        neighboring_coordinate) == "~":
                    self.add_block_to_board(neighboring_coordinate)

    def check_if_coordinates_accessible_to_add_ship(self, ship_coordinates):
        for coordinate in ship_coordinates:
            if self.get_symbol_from_player_board(coordinate) in [";", "O"]:
                return False
            if not self.check_if_coordinate_within_board_border(coordinate):
                return False
        else:
            return True

    def check_if_coordinate_within_board_border(self, coordinate):
        if coordinate["row"] in self.row_index and coordinate["column"] in range(1, self.size_columns + 1):
            return True
        else:
            return False

    def get_row_from_index(self, index):
        for row, value in self.row_index.items():
            if index == value:
                return row
        return None

    def get_index_from_row(self, row_letter):
        for row, index in self.row_index.items():
            if row_letter == row:
                return index
        return None

    def add_block_to_board(self, coordinate):
        if self.check_if_coordinate_within_board_border(coordinate):
            self.update_player_board(coordinate, ";")

    def remove_blocks_from_board(self):
        for row in self.row_index:
            for column in range(1, self.size_columns + 1):
                coordinate = {"row": row, "column": column}
                if self.get_symbol_from_player_board(coordinate) == ";":
                    self.update_player_board(coordinate, "~")

    def add_result_of_player_shot_into_opponent_board(self, coordinate, result):
        if self.check_if_coordinate_within_board_border(coordinate):
            if result == "HIT":
                self.update_opponent_board(coordinate, 'X')
            elif result == "MISS":
                self.update_opponent_board(coordinate, 'M')
            elif result == "SINKING":
                coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(coordinate)
                for coordinate in coordinates_of_sunk_ship:
                    self.update_opponent_board(coordinate, "S")

    def result_of_opponent_shot(self, coordinate):
        if self.check_if_coordinate_within_board_border(coordinate):
            if self.get_symbol_from_player_board(coordinate) == "O":
                ship = self.get_ship_by_coordinate(coordinate)
                ship.make_damage_for_ship()
                self.ships.check_ship_durability(ship)
                if ship.ship_durability == 0:
                    result = "SINKING"
                    self.mark_opponent_shot_result_into_player_board(coordinate, result)
                    return result
                else:
                    result = "HIT"
                    self.mark_opponent_shot_result_into_player_board(coordinate, result)
                    return result
            elif self.get_symbol_from_player_board(coordinate) in ["~", ";"]:
                result = "MISS"
                self.mark_opponent_shot_result_into_player_board(coordinate, result)
                return result
            elif self.get_symbol_from_player_board(coordinate) == "X":
                result = "REPEATED SHOT"
                self.mark_opponent_shot_result_into_player_board(coordinate, result)
                return result
        else:
            return "The shot is not within the boundaries of the board."

    def get_ship_by_coordinate(self, coordinate):
        for ship in [*self.ships.active_ships, *self.ships.destroyed_ships]:
            if coordinate in ship.coordinates:
                return ship

    def mark_opponent_shot_result_into_player_board(self, coordinate, result):
        if result == "MISS":
            self.update_player_board(coordinate, "M")
        elif result == "HIT":
            self.update_player_board(coordinate, "X")
        elif result == "REPEATED SHOT":
            pass
        elif result == "SINKING":
            sunk_ship = self.get_ship_by_coordinate(coordinate)
            for coordinate_of_sunk_ship in sunk_ship.coordinates:
                self.update_player_board(coordinate_of_sunk_ship, "S")

    def prepare_board_for_game_start(self):
        self.remove_blocks_from_board()
        self.draw_player_board()
        self.draw_opponent_board()

    def reload_boards(self):
        self.draw_player_board()
        self.draw_opponent_board()

    def get_coordinates_of_sunk_ship_from_last_hit_coordinate(self, last_hit_coordinate_of_sunk_ship):
        row, column = self.get_row_and_column_from_coordinate(last_hit_coordinate_of_sunk_ship)
        row_index = self.get_index_from_row(row)
        coordinates_with_row_index = [[{"row_index": row_index, "column": column - distance, "direction": "left"},
                                       {"row_index": row_index, "column": column + distance, "direction": "right"},
                                       {"row_index": row_index - distance, "column": column, "direction": "up"},
                                       {"row_index": row_index + distance, "column": column, "direction": "down"}] for
                                      distance in range(1, 4)]

        neighboring_coordinates_with_row_index = [coordinate for distance in coordinates_with_row_index for
                                                  coordinate in distance]

        directions = ['left', 'right', 'up', 'down']

        coordinates_of_sunk_ship = [last_hit_coordinate_of_sunk_ship]
        for direction in directions:
            side_neighboring_coordinates_with_row_index = list(
                filter(lambda x: x["direction"] == direction, neighboring_coordinates_with_row_index))
            if direction == "left":
                side_neighboring_coordinates_with_row_index.sort(key=lambda x: x["column"], reverse=True)
            if direction == "right":
                side_neighboring_coordinates_with_row_index.sort(key=lambda x: x["column"])
            if direction == "up":
                side_neighboring_coordinates_with_row_index.sort(key=lambda x: x["row_index"], reverse=True)
            if direction == "down":
                side_neighboring_coordinates_with_row_index.sort(key=lambda x: x["row_index"])
            for neighboring_coordinate_with_row_index in side_neighboring_coordinates_with_row_index:
                coordinate = self.get_coordinate_from_coordinate_with_row_index(neighboring_coordinate_with_row_index)
                if coordinate:
                    if self.get_symbol_from_opponent_board(coordinate) == "X":
                        coordinates_of_sunk_ship.append(coordinate)
                    else:
                        break
                else:
                    break
        return coordinates_of_sunk_ship

    def get_neighboring_coordinates_in_four_directions(self, coordinate):
        row, column = self.get_row_and_column_from_coordinate(coordinate)
        row_index = self.get_index_from_row(row)
        neighboring_coordinates_with_row_index = [{"row_index": row_index, "column": column - 1},
                                                  {"row_index": row_index, "column": column + 1},
                                                  {"row_index": row_index - 1, "column": column},
                                                  {"row_index": row_index + 1, "column": column}]
        neighboring_coordinates = []
        for coordinate_with_row_index in neighboring_coordinates_with_row_index:
            coordinate = self.get_coordinate_from_coordinate_with_row_index(coordinate_with_row_index)
            if coordinate:
                neighboring_coordinates.append(coordinate)
        return neighboring_coordinates

    def get_neighboring_coordinates_in_eight_directions(self, coordinate):
        row, column = self.get_row_and_column_from_coordinate(coordinate)
        row_index = self.get_index_from_row(row)
        neighboring_coordinates_with_row_index = [{"row_index": row_index, "column": column - 1},
                                                  {"row_index": row_index, "column": column + 1},
                                                  {"row_index": row_index - 1, "column": column},
                                                  {"row_index": row_index + 1, "column": column},
                                                  {"row_index": row_index - 1, "column": column - 1},
                                                  {"row_index": row_index - 1, "column": column + 1},
                                                  {"row_index": row_index + 1, "column": column - 1},
                                                  {"row_index": row_index + 1, "column": column + 1}]
        neighboring_coordinates = []
        for coordinate_with_row_index in neighboring_coordinates_with_row_index:
            coordinate = self.get_coordinate_from_coordinate_with_row_index(coordinate_with_row_index)
            if coordinate:
                neighboring_coordinates.append(coordinate)
        return neighboring_coordinates

    def get_coordinate_from_coordinate_with_row_index(self, coordinate_with_row_index):
        coordinate = {
            "row": self.get_row_from_index(coordinate_with_row_index["row_index"]),
            "column": coordinate_with_row_index["column"]
        }
        if self.check_if_coordinate_within_board_border(coordinate):
            return coordinate

    def get_positions_of_all_ships(self):
        return self.ships.get_ships_coordinates_on_board()

    def update_player_board(self, coordinate, symbol):
        try:
            row, column = self.get_row_and_column_from_coordinate(coordinate)
        except TypeError:
            return None
        else:
            self.player_board[row][column] = symbol

    def update_opponent_board(self, coordinate, symbol):
        try:
            row, column = self.get_row_and_column_from_coordinate(coordinate)
        except TypeError:
            return None
        else:
            self.opponent_board[row][column] = symbol

    def get_symbol_from_player_board(self, coordinate):
        try:
            row, column = self.get_row_and_column_from_coordinate(coordinate)
        except TypeError:
            return None
        else:
            symbol = self.player_board[row][column]
            return symbol

    def get_symbol_from_opponent_board(self, coordinate):
        try:
            row, column = self.get_row_and_column_from_coordinate(coordinate)
        except TypeError:
            return None
        else:
            symbol = self.opponent_board[row][column]
            return symbol

    def get_row_and_column_from_coordinate(self, coordinate):
        if self.check_if_coordinate_within_board_border(coordinate):
            return coordinate["row"], coordinate["column"]
        else:
            return None

class BoardAI(Board):

    def __init__(self):
        super().__init__()
        self.possible_shots_for_player_ai = self.get_starting_possible_shots()

    def get_starting_possible_shots(self):
        shots_to_take = {"priority": [],
                         "normal": [{"row": row, "column": column}
                                    for row in self.row_index for column in range(1, self.size_columns + 1)]}
        return shots_to_take

    def add_result_of_player_shot_into_opponent_board(self, coordinate, result):
        if self.check_if_coordinate_within_board_border(coordinate):
            if result == "HIT":
                self.update_opponent_board(coordinate, 'X')
                self.update_possible_shots_for_player_ai_after_ship_hit(coordinate)
            elif result == "MISS":
                self.update_opponent_board(coordinate, 'M')
                self.update_possible_shots_for_player_ai_after_miss_hit(coordinate)
            elif result == "SINKING":
                self.update_possible_shots_for_player_ai_after_ship_sunk(coordinate)
                coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(coordinate)
                for coordinate in coordinates_of_sunk_ship:
                    self.update_opponent_board(coordinate, "S")

    def update_possible_shots_for_player_ai_after_ship_hit(self, coordinate):
        neighboring_coordinates = self.get_neighboring_coordinates_in_four_directions(coordinate)
        for neighboring_coordinate in neighboring_coordinates:
            self.upgrade_priority_of_coordinate_shot_for_possible_shots_for_player_ai(neighboring_coordinate)
        self.remove_coordinate_from_possible_shots_for_player_ai(coordinate)

    def update_possible_shots_for_player_ai_after_ship_sunk(self, coordinate):
        coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(coordinate)
        for coordinate_of_sunk_ship in coordinates_of_sunk_ship:
            self.remove_coordinate_from_possible_shots_for_player_ai(coordinate_of_sunk_ship)
            neighboring_coordinates_of_part_of_sunk_ship = self.get_neighboring_coordinates_in_eight_directions(
                coordinate_of_sunk_ship)
            for neighboring_coordinate in neighboring_coordinates_of_part_of_sunk_ship:
                self.remove_coordinate_from_possible_shots_for_player_ai(neighboring_coordinate)

    def update_possible_shots_for_player_ai_after_miss_hit(self, coordinate):
        self.remove_coordinate_from_possible_shots_for_player_ai(coordinate)

    def remove_coordinate_from_possible_shots_for_player_ai(self, coordinate):
        if coordinate in self.possible_shots_for_player_ai["priority"]:
            self.possible_shots_for_player_ai["priority"].remove(coordinate)
        if coordinate in self.possible_shots_for_player_ai["normal"]:
            self.possible_shots_for_player_ai["normal"].remove(coordinate)

    def upgrade_priority_of_coordinate_shot_for_possible_shots_for_player_ai(self, coordinate):
        if coordinate in self.possible_shots_for_player_ai["normal"]:
            self.possible_shots_for_player_ai["priority"].append(coordinate)
            self.possible_shots_for_player_ai["normal"].remove(coordinate)


if __name__ == "__main__":
    board = Board()
