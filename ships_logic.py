import string


class Ship:
    def __init__(self, row, column, size, orientation):
        self.row = row
        self.column = column
        self.size = size
        self.orientation = orientation
        self.rows_list = []
        self.columns_list = []
        self.add_rows_to_list = self.establish_ship_rows()
        self.add_column_to_list = self.establish_ship_columns()
        self.ship_durability = self.size

    def ship_hit(self):
        self.ship_durability -= 1
        return self.ship_durability

    def establish_ship_rows(self):
        if self.orientation == "horizontal":
            self.rows_list.append(self.row)
        elif self.orientation == "vertical":
            row_index = self.find_row_letter_index(self.row)
            for i in range(row_index, row_index + self.size):
                letter = string.ascii_uppercase[i]
                self.rows_list.append(letter)
        return self.rows_list

    def establish_ship_columns(self):
        if self.orientation == "horizontal":
            for i in range(self.column, self.column + self.size):
                self.columns_list.append(i)
        elif self.orientation == "vertical":
            self.columns_list.append(self.column)
        return self.columns_list

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

    def move_ships_from_ships_type_quantity_list_to_ships_deploy_list(self):
        new_list = []
        items_to_remove = []
        for item in self.ships_type_quantity_list:
            if isinstance(item, list):
                for subitem in item:
                    new_list.append(subitem)
                items_to_remove.append(item)
            else:
                new_list.append(item)
                items_to_remove.append(item)
        for item in items_to_remove:
            self.ships_type_quantity_list.remove(item)
        self.ships_to_deploy_list = new_list
