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
            row_index = Ship.find_row_letter_index(self.row)
            for index in range(row_index, row_index + self.size):
                row = string.ascii_uppercase[index]
                coordinate = {"row": row, "column": self.column}
                coordinates.append(coordinate)
        return coordinates

    @staticmethod
    def find_row_letter_index(row):
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
        self.active_ships = []
        self.destroyed_ships = []
        self.ships_type_quantity_list = [
            "Four-masted ship",
            ["Three-masted ship" for _ in range(2)],
            ["Two-masted ship" for _ in range(3)],
            ["One-masted ship" for _ in range(4)]
        ]
        self.ships_to_deploy_list = []
        self.move_ships_from_ships_type_quantity_list_to_ships_deploy_list()

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

    def check_ship_durability(self, ship):
        if ship.ship_durability == 0:
            self.destroyed_ships.append(ship)
            self.active_ships.remove(ship)

    def get_ships_coordinates_on_board(self):
        final_board_coordinates = {"Four-masted ship": [],
                                   "Three-masted ship": [],
                                   "Two-masted ship": [],
                                   "One-masted ship": []}
        for ship in [*self.active_ships, *self.destroyed_ships]:
            if ship.size == 1:
                row = ship.coordinates[0]["row"]
                column = str(ship.coordinates[0]["column"])
                formatted_coordinate = ''.join([row, column])
                final_board_coordinates["One-masted ship"].append(formatted_coordinate)
            else:
                row_begin = ship.coordinates[0]["row"]
                column_begin = str(ship.coordinates[0]["column"])
                row_end = ship.coordinates[-1]["row"]
                column_end = str(ship.coordinates[-1]["column"])
                formatted_coordinate = f"{row_begin}{column_begin}-{row_end}{column_end}"
                if ship.size == 4:
                    final_board_coordinates["Four-masted ship"].append(formatted_coordinate)
                if ship.size == 3:
                    final_board_coordinates["Three-masted ship"].append(formatted_coordinate)
                if ship.size == 2:
                    final_board_coordinates["Two-masted ship"].append(formatted_coordinate)
        return final_board_coordinates
