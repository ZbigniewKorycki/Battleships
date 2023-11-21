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

        coordinate_1 = self.board.check_if_coordinate_within_board_border({"row": "A", "column": 1})
        coordinate_2 = self.board.check_if_coordinate_within_board_border({"row": "A", "column": 10})
        coordinate_3 = self.board.check_if_coordinate_within_board_border({"row": "J", "column": 1})
        coordinate_4 = self.board.check_if_coordinate_within_board_border({"row": "J", "column": 10})
        coordinate_5 = self.board.check_if_coordinate_within_board_border({"row": "A", "column": 11})
        coordinate_6 = self.board.check_if_coordinate_within_board_border({"row": "K", "column": 1})
        coordinate_7 = self.board.check_if_coordinate_within_board_border({"row": "AA", "column": 1})
        coordinate_8 = self.board.check_if_coordinate_within_board_border({"row": "a", "column": 2})
        coordinate_9 = self.board.check_if_coordinate_within_board_border({"row": 5, "column": 5})
        coordinate_10 = self.board.check_if_coordinate_within_board_border({"row": 0, "column": 0})
        coordinate_11 = self.board.check_if_coordinate_within_board_border({"row": "A", "column": "A"})
        self.assertTrue(coordinate_1)
        self.assertTrue(coordinate_2)
        self.assertTrue(coordinate_3)
        self.assertTrue(coordinate_4)
        self.assertFalse(coordinate_5)
        self.assertFalse(coordinate_6)
        self.assertFalse(coordinate_7)
        self.assertFalse(coordinate_8)
        self.assertFalse(coordinate_9)
        self.assertFalse(coordinate_10)
        self.assertFalse(coordinate_11)

    def test_get_row_from_index(self):
        row_1 = self.board.get_row_from_index(1)
        row_2 = self.board.get_row_from_index(10)
        row_3 = self.board.get_row_from_index(0)
        row_4 = self.board.get_row_from_index(11)
        row_5 = self.board.get_row_from_index("A")
        row_6 = self.board.get_row_from_index("J")
        self.assertEqual("A", row_1)
        self.assertEqual("J", row_2)
        self.assertIs(row_3, None)
        self.assertIs(row_4, None)
        self.assertIs(row_5, None)
        self.assertIs(row_6, None)

    def test_get_index_from_row(self):
        index_1 = self.board.get_index_from_row(1)
        index_2 = self.board.get_index_from_row(0)
        index_3 = self.board.get_index_from_row("A")
        index_4 = self.board.get_index_from_row("J")
        index_5 = self.board.get_index_from_row("a")
        index_6 = self.board.get_index_from_row("Z")
        self.assertIs(index_1, None)
        self.assertIs(index_2, None)
        self.assertEqual(1, index_3)
        self.assertEqual(10, index_4)
        self.assertIs(index_5, None)
        self.assertIs(index_6, None)

    def test_add_block_to_board(self):
        correct_coordinate = {"row": "B", "column": 5}
        incorrect_coordinate_wrong_row = {"row": "Z", "column": 1}
        incorrect_coordinate_wrong_column = {"row": "A", "column": 100}

        self.board.add_block_to_board(correct_coordinate)
        self.board.add_block_to_board(incorrect_coordinate_wrong_row)
        self.board.add_block_to_board(incorrect_coordinate_wrong_column)

        self.assertEqual(";", self.board.get_symbol_from_player_board(correct_coordinate))
        self.assertRaises(KeyError, self.board.get_symbol_from_player_board, incorrect_coordinate_wrong_row)
        self.assertRaises(KeyError, self.board.get_symbol_from_player_board, incorrect_coordinate_wrong_column)

