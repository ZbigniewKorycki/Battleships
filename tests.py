import unittest
from board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()


    def tearDown(self) -> None:
        pass

    def test_create_starting_board(self):
        new_board = self.board.create_starting_board()
        number_of_rows = self.board.size_rows
        number_of_columns = self.board.size_columns
        self.assertIsInstance(new_board, dict)
        self.assertEqual(len(new_board), number_of_rows)
        self.assertEqual(len(new_board["A"]), number_of_columns)
