import string


class Board:
    def __init__(self, size_rows=10, size_columns=10):
        self.size_rows = size_rows
        self.size_columns = size_columns
        self.board = self.create_starting_board()
        self.draw_board()

    def create_starting_board(self):
        starting_board = {
            row: {col: "~" for col in range(1, self.size_columns + 1)}
            for row in string.ascii_uppercase[0 : self.size_rows]
        }
        return starting_board

    def draw_board(self):
        print(end="  ")
        columns = [print(num, end=" ") for num in range(1, self.size_columns + 1)]
        print()
        rows_with_value = [
            print(letter, " ".join(list(row.values())))
            for letter, row in self.board.items()
        ]


if __name__ == "__main__":
    board = Board()
