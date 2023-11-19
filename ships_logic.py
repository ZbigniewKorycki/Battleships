import string


class Ship:
    def __init__(self, row, column, size, orientation):
        self.row = row
        self.column = column
        self.size = size
        self.orientation = orientation
        self.coordinates = self.get_coordinates_of_ship()
        self.ship_durability = self.size

    def make_damage_for_ship(self):
        self.ship_durability -= 1

    def get_coordinates_of_ship(self):
        coordinates = []
        if self.orientation == 'horizontal':
            for column in range(self.column, self.column + self.size):
                coordinate = {"row": self.row, "column": column}
                coordinates.append(coordinate)
        elif self.orientation == "vertical":
            row_index = self.find_row_letter_index(self.row)
            for index in range(row_index, row_index + self.size):
                row = string.ascii_uppercase[index]
                coordinate = {"row": row, "column": self.column}
                coordinates.append(coordinate)
        return coordinates

    def find_row_letter_index(self, row):
        for letter in string.ascii_uppercase:
            if letter == row:
                row_index = string.ascii_uppercase.index(row)
                return row_index

    def __str__(self):
        if self.orientation == "horizontal":
            return f"{self.row}{self.column} - {self.row}{self.column - 1 + self.size}"
        elif self.orientation == "vertical":
            return f"{self.row}{self.column} - {string.ascii_uppercase[string.ascii_uppercase.index(self.row) - 1 + self.size]}{self.column}"

    def __repr__(self):
        return str(self)


class Ships:
    def __init__(self):
        self.ships_list = []
        self.destroyed_ships_list = []
        self.ships_type_quantity_list = [
            "Four-masted ship",
            ["Three-masted ship" for _ in range(2)],
            ["Two-masted ship" for _ in range(3)],
            ["One-masted ship" for _ in range(4)]
        ]
        self.ships_to_deploy_list = []
        self.ships_type_quantity_list_order = self.move_ships_from_ships_type_quantity_list_to_ships_deploy_list()
        self.ships_coordinates_on_board = {}

    def move_ships_from_ships_type_quantity_list_to_ships_deploy_list(self):
        new_ships_list = []
        ships_to_remove = []
        for item in self.ships_type_quantity_list:
            if isinstance(item, list):
                for subitem in item:
                    new_ships_list.append(subitem)
                ships_to_remove.append(item)
            else:
                new_ships_list.append(item)
                ships_to_remove.append(item)
        for item in ships_to_remove:
            self.ships_type_quantity_list.remove(item)
        self.ships_to_deploy_list = new_ships_list

    def save_ships_coordinates(self, ship_type, ship):
        if ship_type in ["Four-masted ship", "Three-masted ship", "Two-masted ship", "One-masted ship"]:
            if ship_type not in self.ships_coordinates_on_board:
                self.ships_coordinates_on_board[ship_type] = []
            self.ships_coordinates_on_board[ship_type].append(str(ship))

    def check_ship_durability(self, ship):
        if ship.ship_durability == 0:
            self.destroyed_ships_list.append(ship)
            self.ships_list.remove(ship)
