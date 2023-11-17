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
        self.possible_shots_for_ai = self.get_starting_possible_shots()

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
        numbers_of_sunk_signs = sum([1 for key_outer, inner_dict in self.opponent_board.items() for key_inner, value in inner_dict.items() if value == "S"])
        return numbers_of_sunk_signs

    def add_ship(self, ship):
        if self.check_if_coordinates_accessible_to_add_ship(ship.coordinates):
            for coordinate in ship.coordinates:
                row = coordinate["row"]
                column = coordinate["column"]
                self.player_board[row][column] = "O"
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

    def check_if_coordinates_accessible_to_add_ship(self, ship_coordinates):
        for coordinate in ship_coordinates:
            row = coordinate["row"]
            column = coordinate["column"]
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

    def add_result_of_player_shot_into_opponent_board(self, coordinate, result):
        row = coordinate["row"]
        column = coordinate["column"]
        if self.check_if_coordinate_within_board_border(row, column):
            if result == "HIT":
                self.opponent_board[row][column] = "X"
                self.update_possible_shots_for_ai_after_ship_hit(row, column)
            elif result == "MISS":
                self.opponent_board[row][column] = "M"
                self.update_possible_shots_for_ai_after_miss_hit(row, column)
            elif result == "SINKING":
                coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(row, column)
                for coordinate in coordinates_of_sunk_ship:
                    self.opponent_board[coordinate["row"]][coordinate["column"]] = "S"
                self.update_possible_shots_for_ai_after_ship_sunk(row, column)
        else:
            print("Shot outside board.")

    def result_of_opponent_shot(self, coordinate):
        row = coordinate["row"]
        column = coordinate["column"]
        if self.check_if_coordinate_within_board_border(row, column):
            if self.player_board[row][column] == "O":
                hit_ship = self.get_ship_by_coordinate(row, column)
                if hit_ship.ship_hit() == 0:
                    result = "SINKING"
                    self.mark_opponent_shot_result_into_player_board(coordinate, result)
                    return result
                else:
                    result = "HIT"
                    self.mark_opponent_shot_result_into_player_board(coordinate, result)
                    return result
            elif self.player_board[row][column] == "~" or self.player_board[row][column] == ";":
                result = "MISS"
                self.mark_opponent_shot_result_into_player_board(coordinate, result)
                return result
            elif self.player_board[row][column] == "X":
                result = "REPEATED SHOT"
                self.mark_opponent_shot_result_into_player_board(coordinate, result)
                return result
        else:
            return "The shot is not within the boundaries of the board."

    def get_ship_by_coordinate(self, row, column):
        for ship in self.ships.ships_list:
            if row in ship.rows_list and column in ship.columns_list:
                return ship

    def mark_opponent_shot_result_into_player_board(self, coordinate, result):
        row = coordinate["row"]
        column = coordinate["column"]

        if result == "MISS":
            self.player_board[row][column] = "M"
        elif result == "HIT":
            self.player_board[row][column] = "X"
        elif result == "REPEATED SHOT":
            pass
        elif result == "SINKING":
            sunk_ship = self.get_ship_by_coordinate(row, column)
            for column in sunk_ship.columns_list:
                for row in sunk_ship.rows_list:
                    self.player_board[row][column] = "S"

    def prepare_board_for_game_start(self):
        self.remove_blocks_from_board()
        self.draw_player_board()
        self.draw_opponent_board()

    def reload_boards(self):
        self.draw_player_board()
        self.draw_opponent_board()

    def get_coordinates_of_sunk_ship_from_last_hit_coordinate(self, row, column):
        ship_row_index = self.row_index[row]
        coordinates_of_sunk_ship = [{"row": row, "column": column}]
        direct_neighboring_coordinates = [
            [[ship_row_index, column - 1], [ship_row_index, column - 2], [ship_row_index, column - 3]],  # left
            [[ship_row_index, column + 1], [ship_row_index, column + 2], [ship_row_index, column + 3]],  # right
            [[ship_row_index - 1, column], [ship_row_index - 2, column], [ship_row_index - 3, column]],  # up
            [[ship_row_index + 1, column], [ship_row_index + 2, column], [ship_row_index + 3, column]]]  # down
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

    def get_neighboring_coordinates_from_four_world_directions(self, row, column):
        four_directions_neighboring_coordinates = []
        ship_row_index = self.row_index[row]
        neighboring_coordinates_as_indexes = [[ship_row_index, column - 1], [ship_row_index, column + 1],
                                              [ship_row_index - 1, column], [ship_row_index + 1, column]]
        for coordinate_as_index in neighboring_coordinates_as_indexes:
            neighboring_row_index, neighboring_column = coordinate_as_index
            neighboring_row = self.get_row_from_index(neighboring_row_index)
            if self.check_if_coordinate_within_board_border(neighboring_row, neighboring_column):
                neighboring_coordinate = {
                    "row": neighboring_row,
                    "column": neighboring_column
                }
                four_directions_neighboring_coordinates.append(neighboring_coordinate)
        return four_directions_neighboring_coordinates

    def get_all_neighboring_coordinates_of_coordinate(self, row, column):
        all_neighboring_coordinates = []
        ship_row_index = self.row_index[row]
        neighboring_coordinates_as_indexes = [[ship_row_index, column - 1], [ship_row_index, column + 1],
                                              [ship_row_index - 1, column], [ship_row_index + 1, column],
                                              [ship_row_index - 1, column - 1], [ship_row_index - 1, column + 1],
                                              [ship_row_index + 1, column - 1], [ship_row_index + 1, column + 1]]
        for coordinate_as_index in neighboring_coordinates_as_indexes:
            neighboring_row_index, neighboring_column = coordinate_as_index
            neighboring_row = self.get_row_from_index(neighboring_row_index)
            if self.check_if_coordinate_within_board_border(neighboring_row, neighboring_column):
                neighboring_coordinate = {
                    "row": neighboring_row,
                    "column": neighboring_column
                }
                all_neighboring_coordinates.append(neighboring_coordinate)
        return all_neighboring_coordinates

    def get_positions_of_all_ships(self):
        return self.ships.ships_coordinates_on_board

    def get_starting_possible_shots(self):
        shots_to_take = {"priority": [],
                         "normal": [{"row": row, "column": column}
                                    for row in self.row_index for column in range(1, self.size_columns + 1)]}
        return shots_to_take

    def update_possible_shots_for_ai_after_ship_hit(self, row, column):
        neighboring_coordinates = self.get_neighboring_coordinates_from_four_world_directions(row, column)
        for coordinate in neighboring_coordinates:
            self.upgrade_priority_of_coordinate_shot_for_possible_shots_for_ai(coordinate)
        self.remove_coordinate_from_possible_shots_for_ai(self.get_coordinate_from_row_and_column(row, column))

    def update_possible_shots_for_ai_after_ship_sunk(self, row, column):
        coordinates_of_sunk_ship = self.get_coordinates_of_sunk_ship_from_last_hit_coordinate(row, column)
        for coordinate_of_sunk_ship in coordinates_of_sunk_ship:
            self.remove_coordinate_from_possible_shots_for_ai(coordinate_of_sunk_ship)
            sunk_ship_coordinate_row = coordinate_of_sunk_ship["row"]
            sunk_ship_coordinate_column = coordinate_of_sunk_ship["column"]
            neighboring_coordinates_of_part_of_sunk_ship = self.get_all_neighboring_coordinates_of_coordinate(
                sunk_ship_coordinate_row, sunk_ship_coordinate_column)
            for coordinate in neighboring_coordinates_of_part_of_sunk_ship:
                self.remove_coordinate_from_possible_shots_for_ai(coordinate)

    def update_possible_shots_for_ai_after_miss_hit(self, row, column):
        coordinate = self.get_coordinate_from_row_and_column(row, column)
        self.remove_coordinate_from_possible_shots_for_ai(coordinate)

    def remove_coordinate_from_possible_shots_for_ai(self, coordinate):
        if coordinate in self.possible_shots_for_ai["priority"]:
            self.possible_shots_for_ai["priority"].remove(coordinate)
        if coordinate in self.possible_shots_for_ai["normal"]:
            self.possible_shots_for_ai["normal"].remove(coordinate)

    def upgrade_priority_of_coordinate_shot_for_possible_shots_for_ai(self, coordinate):
        if coordinate in self.possible_shots_for_ai["normal"]:
            self.possible_shots_for_ai["priority"].append(coordinate)
            self.possible_shots_for_ai["normal"].remove(coordinate)

    def get_coordinate_from_row_and_column(self, row, column):
        coordinate = {"row": row,
                      "column": column}
        return coordinate


if __name__ == "__main__":
    board = Board()
