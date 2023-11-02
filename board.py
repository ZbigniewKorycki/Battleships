import string
from ships_logic import Ships


class Board:
    def __init__(self, size_rows=10, size_columns=10):
        self.size_rows = size_rows
        self.size_columns = size_columns
        self.board = self.create_starting_board()
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
        columns = print(end="  "), [print(num, end=" ") for num in range(1, self.size_columns + 1)], print()
        rows_with_value = [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.board.items()
        ]

    def verify_adding_ship(self, coordinates):
        for coordinate in coordinates:
            #ships cant touch each - one row/column of space
            #coordinates have to be inside board
            pass

    def add_ship(self, ship):
        check_another_ship_in_area = self.check_if_ship_under_coordinate(ship.row, ship.column)
        print(check_another_ship_in_area)
        if check_another_ship_in_area == True:
            if ship.orientation == "horizontal":
                for i in range(ship.size):
                    self.board[ship.row][ship.column + i] = "O"
            elif ship.orientation == "vertical":
                rows_indexes = self.row_index[ship.row]
                for i in range(ship.size):
                    letter_index = rows_indexes + i
                    for key, value in self.row_index.items():
                        if value == letter_index:
                            self.board[key][ship.column] = "O"
            self.block_ship_near_fields(ship)
            self.ships.ships_list.append(ship)
            return self.draw_board()
        elif check_another_ship_in_area == False:
            print("There`s another ship in area, try again")

    def block_ship_near_fields(self, ship):
        ship_row_index = self.row_index[ship.row]
        upper_row_index = ship_row_index - 1
        down_row_index_horizontal = ship_row_index + 1
        down_row_index_vertical = ship_row_index + ship.size
        if ship.orientation == "horizontal":
            self.board[ship.row][ship.column - 1] = ";"
            self.board[ship.row][ship.column + ship.size] = ";"
            for key, value in self.row_index.items():
                if value == upper_row_index:
                    for i in range(ship.size):
                        self.board[key][ship.column + i] = ";"
                        self.board[key][ship.column - 1] = ";"
                        self.board[key][ship.column + ship.size] = ";"
            for key, value in self.row_index.items():
                if value == down_row_index_horizontal:
                    for i in range(ship.size):
                        self.board[key][ship.column + i] = ";"
                        self.board[key][ship.column - 1] = ";"
                        self.board[key][ship.column + ship.size] = ";"
        elif ship.orientation == "vertical":
            for key, value in self.row_index.items():
                if value == upper_row_index:
                    self.board[key][ship.column] = ";"
                    self.board[key][ship.column - 1] = ";"
                    self.board[key][ship.column + 1] = ";"
            for key, value in self.row_index.items():
                if value == down_row_index_vertical:
                    self.board[key][ship.column] = ";"
                    self.board[key][ship.column - 1] = ";"
                    self.board[key][ship.column + 1] = ";"
            for i in range(ship.size):
                letter_index = ship_row_index + i
                for key, value in self.row_index.items():
                    if value == letter_index:
                        self.board[key][ship.column - 1] = ";"
            for i in range(ship.size):
                letter_index = ship_row_index + i
                for key, value in self.row_index.items():
                    if value == letter_index:
                        self.board[key][ship.column + 1] = ";"

    def check_if_ship_under_coordinate(self, row, column):
        if row == "O" or column == "O" or row == ";" or column == ";":
            return False
        else:
            return True





if __name__ == "__main__":
    board = Board()
