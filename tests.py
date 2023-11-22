import unittest
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def tearDown(self) -> None:
        pass

    def test_create_starting_board(self):
        new_board = self.board.create_starting_board()

        self.assertIsInstance(new_board, dict)
        self.assertEqual(len(new_board), self.board.size_rows)
        self.assertEqual(len(new_board["A"]), self.board.size_columns)

    def test_check_if_coordinate_within_board_border(self):
        # rows A-J, columns 1-10

        coordinate_correct_first_row_first_column = self.board.check_if_coordinate_within_board_border(
            {"row": "A", "column": 1})
        coordinate_correct_first_row_last_column = self.board.check_if_coordinate_within_board_border(
            {"row": "A", "column": 10})
        coordinate_correct_last_row_first_column = self.board.check_if_coordinate_within_board_border(
            {"row": "J", "column": 1})
        coordinate_correct_last_row_last_column = self.board.check_if_coordinate_within_board_border(
            {"row": "J", "column": 10})
        coordinate_incorrect_column_of_of_range = self.board.check_if_coordinate_within_board_border(
            {"row": "A", "column": 11})
        coordinate_incorrect_row_of_of_range = self.board.check_if_coordinate_within_board_border(
            {"row": "K", "column": 1})
        coordinate_incorrect_double_row = self.board.check_if_coordinate_within_board_border({"row": "AA", "column": 1})
        coordinate_incorrect_row_lowercase = self.board.check_if_coordinate_within_board_border(
            {"row": "a", "column": 2})
        coordinate_incorrect_row_as_numeric = self.board.check_if_coordinate_within_board_border(
            {"row": 5, "column": 5})
        coordinate_incorrect_column_as_letter = self.board.check_if_coordinate_within_board_border(
            {"row": "A", "column": "A"})

        self.assertTrue(coordinate_correct_first_row_first_column)
        self.assertTrue(coordinate_correct_first_row_last_column)
        self.assertTrue(coordinate_correct_last_row_first_column)
        self.assertTrue(coordinate_correct_last_row_last_column)
        self.assertFalse(coordinate_incorrect_column_of_of_range)
        self.assertFalse(coordinate_incorrect_row_of_of_range)
        self.assertFalse(coordinate_incorrect_double_row)
        self.assertFalse(coordinate_incorrect_row_lowercase)
        self.assertFalse(coordinate_incorrect_row_as_numeric)
        self.assertFalse(coordinate_incorrect_column_as_letter)

    def test_get_row_from_index(self):
        correct_index_first = self.board.get_row_from_index(1)
        correct_index_last = self.board.get_row_from_index(10)
        incorrect_index_out_of_range_minus = self.board.get_row_from_index(-1)
        incorrect_index_out_of_range = self.board.get_row_from_index(11)
        incorrect_index_letter = self.board.get_row_from_index("A")
        self.assertEqual("A", correct_index_first)
        self.assertEqual("J", correct_index_last)
        self.assertIs(incorrect_index_out_of_range_minus, None)
        self.assertIs(incorrect_index_out_of_range, None)
        self.assertIs(incorrect_index_letter, None)

    def test_get_index_from_row(self):
        correct_row_a = self.board.get_index_from_row("A")
        correct_row_j = self.board.get_index_from_row("J")
        incorrect_row_as_number = self.board.get_index_from_row(1)
        incorrect_row_lowercase = self.board.get_index_from_row("a")
        incorrect_row_out_of_range = self.board.get_index_from_row("Z")

        self.assertEqual(1, correct_row_a)
        self.assertEqual(10, correct_row_j)
        self.assertIs(incorrect_row_as_number, None)
        self.assertIs(incorrect_row_lowercase, None)
        self.assertIs(incorrect_row_out_of_range, None)

    def test_add_block_to_board(self):
        correct_coordinate = {"row": "B", "column": 5}
        incorrect_coordinate_wrong_row = {"row": "Z", "column": 1}
        incorrect_coordinate_wrong_column = {"row": "A", "column": 100}

        self.board.add_block_to_board(correct_coordinate)
        self.board.add_block_to_board(incorrect_coordinate_wrong_row)
        self.board.add_block_to_board(incorrect_coordinate_wrong_column)

        self.assertEqual(";", self.board.get_symbol_from_player_board(correct_coordinate))
        self.assertRaises(TypeError, self.board.get_symbol_from_player_board, incorrect_coordinate_wrong_row)
        self.assertRaises(TypeError, self.board.get_symbol_from_player_board, incorrect_coordinate_wrong_column)

    def test_remove_blocks_from_board(self):
        coordinate_1 = {"row": "B", "column": 5}
        coordinate_2 = {"row": "A", "column": 5}
        coordinate_3 = {"row": "J", "column": 10}

        self.board.add_block_to_board(coordinate_1)
        self.board.add_block_to_board(coordinate_2)
        self.board.add_block_to_board(coordinate_3)

        self.assertEqual(";", self.board.get_symbol_from_player_board(coordinate_1))
        self.assertEqual(";", self.board.get_symbol_from_player_board(coordinate_2))
        self.assertEqual(";", self.board.get_symbol_from_player_board(coordinate_3))

        self.board.remove_blocks_from_board()

        self.assertNotEquals(";", self.board.get_symbol_from_player_board(coordinate_1))
        self.assertNotEquals(";", self.board.get_symbol_from_player_board(coordinate_2))
        self.assertNotEquals(";", self.board.get_symbol_from_player_board(coordinate_3))

        self.assertEqual("~", self.board.get_symbol_from_player_board(coordinate_1))
        self.assertEqual("~", self.board.get_symbol_from_player_board(coordinate_2))
        self.assertEqual("~", self.board.get_symbol_from_player_board(coordinate_3))

    def test_get_neighboring_coordinates_in_four_directions(self):
        # correct coordinate should have 4 neighboring coordinates
        correct_coordinate = {"row": "C", "column": 5}
        self.assertIn({"row": "B", "column": 5},
                      self.board.get_neighboring_coordinates_in_four_directions(correct_coordinate))
        self.assertIn({"row": "D", "column": 5},
                      self.board.get_neighboring_coordinates_in_four_directions(correct_coordinate))
        self.assertIn({"row": "C", "column": 4},
                      self.board.get_neighboring_coordinates_in_four_directions(correct_coordinate))
        self.assertIn({"row": "C", "column": 6},
                      self.board.get_neighboring_coordinates_in_four_directions(correct_coordinate))
        self.assertEqual(4, len(self.board.get_neighboring_coordinates_in_four_directions(correct_coordinate)))

        # incorrect coordinates
        incorrect_coordinate_with_column_out_of_range = {"row": "J", "column": 11}
        self.assertRaises(TypeError, self.board.get_neighboring_coordinates_in_four_directions,
                          incorrect_coordinate_with_column_out_of_range)

        incorrect_coordinate_with_row_out_of_range = {"row": "K", "column": 3}
        self.assertRaises(TypeError, self.board.get_neighboring_coordinates_in_four_directions,
                          incorrect_coordinate_with_row_out_of_range)


    def test_get_neighboring_coordinates_in_eight_directions(self):
        #Coordinate of right down corner - should have only 3 neighboring coordinates
        correct_coordinate_right_down_corner = {"row": "J", "column": 10}
        self.assertIn({"row": "I", "column": 10},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_right_down_corner))
        self.assertIn({"row": "J", "column": 9},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_right_down_corner))
        self.assertIn({"row": "I", "column": 9},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_right_down_corner))
        self.assertEqual(3, len(self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_right_down_corner)))

        # Coordinate which should have 8 neighboring coordinates
        correct_coordinate_middle = {"row": "E", "column": 5}
        self.assertIn({"row": "E", "column": 4},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "E", "column": 6},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "D", "column": 4},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "D", "column": 5},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "D", "column": 6},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "F", "column": 4},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "F", "column": 5},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertIn({"row": "F", "column": 6},
                      self.board.get_neighboring_coordinates_in_eight_directions(correct_coordinate_middle))
        self.assertEqual(8, len(self.board.get_neighboring_coordinates_in_eight_directions(
            correct_coordinate_middle)))

        #incorrect coordinates
        incorrect_coordinate_with_column_out_of_range = {"row": "J", "column": 11}
        self.assertRaises(TypeError, self.board.get_neighboring_coordinates_in_eight_directions,
                          incorrect_coordinate_with_column_out_of_range)

        incorrect_coordinate_with_row_out_of_range = {"row": "K", "column": 3}
        self.assertRaises(TypeError, self.board.get_neighboring_coordinates_in_eight_directions,
                          incorrect_coordinate_with_row_out_of_range)
