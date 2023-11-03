import string


class Ship:
    def __init__(self, row, column, size, orientation):
        self.row = row
        self.column = column
        self.size = size
        self.orientation = orientation
        self.ship_durability = self.size

    def ship_hit(self):
        self.ship_durability -= 1
        if self.ship_durability == 0:
            print("ship destroyed")            #add communication protocol latter

    def ship_coordinate(self):
        if self.orientation == "horizontal":
            print(f"{self.row}{self.column} - {self.row}{self.column + self.size - 1}")
        elif self.orientation == "vertical":
            row_letters = string.ascii_uppercase
            ship_row_index = row_letters.index(self.row)
            ship_row_index += self.size
            ship_row_index_end = row_letters[ship_row_index - 1]
            print(f"{self.row}{self.column} - {ship_row_index_end}{self.column}")


class Ships:
    def __init__(self):
        self.ships_list = []
        self.ships_type_quantity = {
            "Four-masted ship": 1,
            "Three-masted ship": 2,
            "Two-masted ship": 3,
            "One-masted ship": 4
        }
