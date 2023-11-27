import string
from ships_logic import Ships
from custom_exception import CustomException


class Board:
    def __init__(self, size_rows=10, size_columns=10):
        self.size_rows = size_rows
        self.size_columns = size_columns
        self.player_board = self.create_starting_board()
        self.opponent_board = self.create_starting_board()
        # self.draw_player_board()
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
            "J": 10,
        }
        self.ships = Ships()

    def board_to_dict(self):
        return dict(self.player_board)

    def print_boards_for_archived_games(self, board):
        column_headings = [" "] + [str(i) for i in range(1, 11)]
        print(" ".join(column_headings))
        for row, inner_dict in board.items():
            row_values = " ".join(inner_dict.values())
            print(row, row_values)

    def create_starting_board(self):
        starting_board = {
            row: {col: "~" for col in range(1, self.size_columns + 1)}
            for row in string.ascii_uppercase[0: self.size_rows]
        }
        return starting_board

    def draw_player_board(self):
        print("Player board:".center(self.size_columns * 2 + 1))
        (
            print(end="  "),
            [print(num, end=" ") for num in range(1, self.size_columns + 1)],
            print(),
        )
        [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.player_board.items()
        ]

    def draw_opponent_board(self):
        print("Opponent board:".center(self.size_columns * 2 + 1))
        (
            print(end="  "),
            [print(num, end=" ") for num in range(1, self.size_columns + 1)],
            print(),
        )
        [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.opponent_board.items()
        ]

    def count_sunk_signs(self, board_type):
        numbers_of_sunk_signs = sum(
            [
                1
                for key_outer, inner_dict in board_type.items()
                for key_inner, value in inner_dict.items()
                if value == "S"
            ]
        )
        return numbers_of_sunk_signs

    def add_ship(self, ship):
        if self.check_if_coords_accessible_to_add_ship(ship.coords):
            for coord in ship.coords:
                self.update_player_board(coord, "O")
            self.block_coords_near_ship(ship.coords)
            self.ships.active_ships.append(ship)
            return True
        else:
            raise CustomException(
                "There's another ship in area or ship not within board border."
            )

    def block_coords_near_ship(self, coords):
        for coord in coords:
            neighb_coords = (
                self.get_neighb_coords_in_eight_directions(coord)
            )
            for neighb_coord in neighb_coords:
                if (
                    neighb_coord not in coords
                    and self.get_symbol_player_board(neighb_coord) == "~"
                ):
                    self.add_block_to_board(neighb_coord)

    def check_if_coords_accessible_to_add_ship(self, ship_coords):
        for coord in ship_coords:
            if self.get_symbol_player_board(coord) in [";", "O"]:
                return False
            if not self.check_if_coord_within_board_border(coord):
                return False
        else:
            return True

    def check_if_coord_within_board_border(self, coord):
        if coord["row"] in self.row_index and coord["column"] in range(
            1, self.size_columns + 1
        ):
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

    def add_block_to_board(self, coord):
        if self.check_if_coord_within_board_border(coord):
            self.update_player_board(coord, ";")

    def remove_blocks_from_board(self):
        for row in self.row_index:
            for column in range(1, self.size_columns + 1):
                coord = {"row": row, "column": column}
                if self.get_symbol_player_board(coord) == ";":
                    self.update_player_board(coord, "~")

    def add_result_of_shot_into_opponent_board(self, coord, result):
        if self.check_if_coord_within_board_border(coord):
            if result == "HIT":
                self.update_opponent_board(coord, "X")
            elif result == "MISS":
                self.update_opponent_board(coord, "M")
            elif result == "SINKING":
                coords_of_sunk_ship = (
                    self.get_coords_of_sunk_ship_from_last_hit_coord(
                        coord
                    )
                )
                for coord in coords_of_sunk_ship:
                    self.update_opponent_board(coord, "S")

    def result_of_opponent_shot(self, coord):
        if self.check_if_coord_within_board_border(coord):
            if self.get_symbol_player_board(coord) == "O":
                ship = self.get_ship_by_coord(coord)
                ship.make_damage_for_ship()
                self.ships.check_ship_durability(ship)
                if ship.ship_durability == 0:
                    result = "SINKING"
                    self.mark_opp_shot_result_into_player_board(coord, result)
                    return result
                else:
                    result = "HIT"
                    self.mark_opp_shot_result_into_player_board(coord, result)
                    return result
            elif self.get_symbol_player_board(coord) in ["~", ";"]:
                result = "MISS"
                self.mark_opp_shot_result_into_player_board(coord, result)
                return result
            elif self.get_symbol_player_board(coord) == "X":
                result = "REPEATED SHOT"
                self.mark_opp_shot_result_into_player_board(coord, result)
                return result
        else:
            return "The shot is not within the boundaries of the board."

    def get_ship_by_coord(self, coord):
        for ship in [*self.ships.active_ships, *self.ships.destroyed_ships]:
            if coord in ship.coords:
                return ship

    def mark_opp_shot_result_into_player_board(self, coord, result):
        if result == "MISS":
            self.update_player_board(coord, "M")
        elif result == "HIT":
            self.update_player_board(coord, "X")
        elif result == "REPEATED SHOT":
            pass
        elif result == "SINKING":
            sunk_ship = self.get_ship_by_coord(coord)
            for coord_of_sunk_ship in sunk_ship.coords:
                self.update_player_board(coord_of_sunk_ship, "S")

    def prepare_board_for_game_start(self):
        self.remove_blocks_from_board()
        self.draw_player_board()
        self.draw_opponent_board()

    def reload_boards(self):
        self.draw_player_board()
        self.draw_opponent_board()

    def get_coords_of_sunk_ship_from_last_hit_coord(
        self, last_hit_coord_of_sunk_ship
    ):
        row, column = self.get_row_and_column_from_coord(
            last_hit_coord_of_sunk_ship
        )
        row_index = self.get_index_from_row(row)
        coords_with_row_index = [
            [
                {
                    "row_index": row_index,
                    "column": column - distance,
                    "direction": "left",
                },
                {
                    "row_index": row_index,
                    "column": column + distance,
                    "direction": "right",
                },
                {
                    "row_index": row_index - distance,
                    "column": column,
                    "direction": "up",
                },
                {
                    "row_index": row_index + distance,
                    "column": column,
                    "direction": "down",
                },
            ]
            for distance in range(1, 4)
        ]

        neighb_coords_with_row_index = [
            coord
            for distance in coords_with_row_index
            for coord in distance
        ]

        directions = ["left", "right", "up", "down"]

        coords_of_sunk_ship = [last_hit_coord_of_sunk_ship]
        for direction in directions:
            side_neighb_coords_with_row_index = list(
                filter(
                    lambda x: x["direction"] == direction,
                    neighb_coords_with_row_index,
                )
            )
            if direction == "left":
                side_neighb_coords_with_row_index.sort(
                    key=lambda x: x["column"], reverse=True
                )
            if direction == "right":
                side_neighb_coords_with_row_index.sort(
                    key=lambda x: x["column"]
                )
            if direction == "up":
                side_neighb_coords_with_row_index.sort(
                    key=lambda x: x["row_index"], reverse=True
                )
            if direction == "down":
                side_neighb_coords_with_row_index.sort(
                    key=lambda x: x["row_index"]
                )
            for (
                neighb_coord_with_row_index
            ) in side_neighb_coords_with_row_index:
                coord = self.get_coord_from_coord_with_row_index(
                    neighb_coord_with_row_index
                )
                if coord:
                    if self.get_symbol_opponent_board(coord) == "X":
                        coords_of_sunk_ship.append(coord)
                    else:
                        break
                else:
                    break
        return coords_of_sunk_ship

    def get_neighb_coords_in_four_directions(self, coord):
        row, column = self.get_row_and_column_from_coord(coord)
        row_index = self.get_index_from_row(row)
        neighb_coords_with_row_index = [
            {"row_index": row_index, "column": column - 1},
            {"row_index": row_index, "column": column + 1},
            {"row_index": row_index - 1, "column": column},
            {"row_index": row_index + 1, "column": column},
        ]
        return self.get_coords_from_list_of_coords_with_row_index(
            neighb_coords_with_row_index
        )

    def get_neighb_coords_in_eight_directions(self, coord):
        row, column = self.get_row_and_column_from_coord(coord)
        row_index = self.get_index_from_row(row)
        neighb_coords_with_row_index = [
            {"row_index": row_index, "column": column - 1},
            {"row_index": row_index, "column": column + 1},
            {"row_index": row_index - 1, "column": column},
            {"row_index": row_index + 1, "column": column},
            {"row_index": row_index - 1, "column": column - 1},
            {"row_index": row_index - 1, "column": column + 1},
            {"row_index": row_index + 1, "column": column - 1},
            {"row_index": row_index + 1, "column": column + 1},
        ]

        return self.get_coords_from_list_of_coords_with_row_index(
            neighb_coords_with_row_index
        )

    def get_coords_from_list_of_coords_with_row_index(
        self, list_of_coords_with_row_index
    ):
        coords = []
        for coord_with_row_index in list_of_coords_with_row_index:
            coord = self.get_coord_from_coord_with_row_index(
                coord_with_row_index
            )
            if coord:
                coords.append(coord)
        return coords

    def get_coord_from_coord_with_row_index(self, coord_with_row_index):
        coord = {
            "row": self.get_row_from_index(coord_with_row_index["row_index"]),
            "column": coord_with_row_index["column"],
        }
        if self.check_if_coord_within_board_border(coord):
            return coord

    def get_positions_of_all_ships(self):
        return self.ships.get_ships_coords_on_board()

    def update_player_board(self, coord, symbol):
        try:
            row, column = self.get_row_and_column_from_coord(coord)
        except TypeError:
            return None
        else:
            self.player_board[row][column] = symbol

    def update_opponent_board(self, coord, symbol):
        try:
            row, column = self.get_row_and_column_from_coord(coord)
        except TypeError:
            return None
        else:
            self.opponent_board[row][column] = symbol

    def get_symbol_player_board(self, coord):
        try:
            row, column = self.get_row_and_column_from_coord(coord)
        except TypeError:
            return None
        else:
            symbol = self.player_board[row][column]
            return symbol

    def get_symbol_opponent_board(self, coord):
        try:
            row, column = self.get_row_and_column_from_coord(coord)
        except TypeError:
            return None
        else:
            symbol = self.opponent_board[row][column]
            return symbol

    def get_row_and_column_from_coord(self, coord):
        if self.check_if_coord_within_board_border(coord):
            return coord["row"], coord["column"]
        else:
            return None


class BoardAI(Board):
    def __init__(self):
        super().__init__()
        self.possible_shots = self.get_starting_possible_shots()

    def get_starting_possible_shots(self):
        shots_to_take = {
            "priority": [],
            "normal": [
                {"row": row, "column": column}
                for row in self.row_index
                for column in range(1, self.size_columns + 1)
            ],
        }
        return shots_to_take

    def add_result_of_shot_into_opponent_board(self, coord, result):
        if self.check_if_coord_within_board_border(coord):
            if result == "HIT":
                self.update_opponent_board(coord, "X")
                self.update_possible_shots_after_ship_hit(coord)
            elif result == "MISS":
                self.update_opponent_board(coord, "M")
                self.update_possible_shots_after_miss_hit(coord)
            elif result == "SINKING":
                self.update_possible_shots_after_ship_sunk(coord)
                coords_of_sunk_ship = (
                    self.get_coords_of_sunk_ship_from_last_hit_coord(
                        coord
                    )
                )
                for coord in coords_of_sunk_ship:
                    self.update_opponent_board(coord, "S")

    def update_possible_shots_after_ship_hit(self, coord):
        neighb_coords = self.get_neighb_coords_in_four_directions(
            coord
        )
        for neighb_coord in neighb_coords:
            self.upgrade_priority_of_coord_shot_for_possible_shots(
                neighb_coord
            )
        self.remove_coord_from_possible_shots(coord)

    def update_possible_shots_after_ship_sunk(self, coord):
        coords_of_sunk_ship = (
            self.get_coords_of_sunk_ship_from_last_hit_coord(coord)
        )
        for coord_of_sunk_ship in coords_of_sunk_ship:
            self.remove_coord_from_possible_shots(
                coord_of_sunk_ship
            )
            neighb_coords_of_part_of_sunk_ship = (
                self.get_neighb_coords_in_eight_directions(
                    coord_of_sunk_ship
                )
            )
            for neighb_coord in neighb_coords_of_part_of_sunk_ship:
                self.remove_coord_from_possible_shots(
                    neighb_coord
                )

    def update_possible_shots_after_miss_hit(self, coord):
        self.remove_coord_from_possible_shots(coord)

    def remove_coord_from_possible_shots(self, coord):
        if coord in self.possible_shots["priority"]:
            self.possible_shots["priority"].remove(coord)
        if coord in self.possible_shots["normal"]:
            self.possible_shots["normal"].remove(coord)

    def upgrade_priority_of_coord_shot_for_possible_shots(
        self, coord
    ):
        if coord in self.possible_shots["normal"]:
            self.possible_shots["priority"].append(coord)
            self.possible_shots["normal"].remove(coord)


if __name__ == "__main__":
    board = Board()
