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


class Ships:
    def __init__(self):
        self.ships_list = []
        self.ships_type_quantity = {
            "Four-masted ship": 1,
            "Three-masted ship": 2,
            "Two-masted ship": 3,
            "One-masted ship": 4
        }
