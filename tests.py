import json
import unittest
from board import Board
from custom_exception import CustomException
from ships_logic import Ship, Ships
from data_utils import DataUtils, DatabaseUtils
from config_variables import test_db_file


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

    def test_check_if_coord_within_board_border(self):
        # rows A-J, columns 1-10

        coord_correct_first_row_first_column = (
            self.board.check_if_coord_within_board_border(
                {"row": "A", "column": 1}
            )
        )
        coord_correct_first_row_last_column = (
            self.board.check_if_coord_within_board_border(
                {"row": "A", "column": 10}
            )
        )
        coord_correct_last_row_first_column = (
            self.board.check_if_coord_within_board_border(
                {"row": "J", "column": 1}
            )
        )
        coord_correct_last_row_last_column = (
            self.board.check_if_coord_within_board_border(
                {"row": "J", "column": 10}
            )
        )
        coord_incorrect_column_of_of_range = (
            self.board.check_if_coord_within_board_border(
                {"row": "A", "column": 11}
            )
        )
        coord_incorrect_row_of_of_range = (
            self.board.check_if_coord_within_board_border(
                {"row": "K", "column": 1}
            )
        )
        coord_incorrect_double_row = (
            self.board.check_if_coord_within_board_border(
                {"row": "AA", "column": 1}
            )
        )
        coord_incorrect_row_lowercase = (
            self.board.check_if_coord_within_board_border(
                {"row": "a", "column": 2}
            )
        )
        coord_incorrect_row_as_numeric = (
            self.board.check_if_coord_within_board_border({"row": 5, "column": 5})
        )
        coord_incorrect_column_as_letter = (
            self.board.check_if_coord_within_board_border(
                {"row": "A", "column": "A"}
            )
        )

        self.assertTrue(coord_correct_first_row_first_column)
        self.assertTrue(coord_correct_first_row_last_column)
        self.assertTrue(coord_correct_last_row_first_column)
        self.assertTrue(coord_correct_last_row_last_column)
        self.assertFalse(coord_incorrect_column_of_of_range)
        self.assertFalse(coord_incorrect_row_of_of_range)
        self.assertFalse(coord_incorrect_double_row)
        self.assertFalse(coord_incorrect_row_lowercase)
        self.assertFalse(coord_incorrect_row_as_numeric)
        self.assertFalse(coord_incorrect_column_as_letter)

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
        correct_coord = {"row": "B", "column": 5}
        incorrect_coord_wrong_row = {"row": "Z", "column": 1}
        incorrect_coord_wrong_column = {"row": "A", "column": 100}

        self.board.add_block_to_board(correct_coord)
        self.board.add_block_to_board(incorrect_coord_wrong_row)
        self.board.add_block_to_board(incorrect_coord_wrong_column)

        self.assertEqual(
            ";", self.board.get_symbol_player_board(correct_coord)
        )
        self.assertIs(
            None,
            self.board.get_symbol_player_board(incorrect_coord_wrong_row),
        )
        self.assertIs(
            None,
            self.board.get_symbol_player_board(incorrect_coord_wrong_column),
        )

    def test_remove_blocks_from_board(self):
        coord_1 = {"row": "B", "column": 5}
        coord_2 = {"row": "A", "column": 5}
        coord_3 = {"row": "J", "column": 10}

        self.board.add_block_to_board(coord_1)
        self.board.add_block_to_board(coord_2)
        self.board.add_block_to_board(coord_3)

        self.assertEqual(";", self.board.get_symbol_player_board(coord_1))
        self.assertEqual(";", self.board.get_symbol_player_board(coord_2))
        self.assertEqual(";", self.board.get_symbol_player_board(coord_3))

        self.board.remove_blocks_from_board()

        self.assertNotEquals(";", self.board.get_symbol_player_board(coord_1))
        self.assertNotEquals(";", self.board.get_symbol_player_board(coord_2))
        self.assertNotEquals(";", self.board.get_symbol_player_board(coord_3))

        self.assertEqual("~", self.board.get_symbol_player_board(coord_1))
        self.assertEqual("~", self.board.get_symbol_player_board(coord_2))
        self.assertEqual("~", self.board.get_symbol_player_board(coord_3))

    def test_get_neighb_coords_in_four_directions(self):
        # Correct coord should have 4 neighboring coords
        correct_coord = {"row": "C", "column": 5}
        self.assertIn(
            {"row": "B", "column": 5},
            self.board.get_neighb_coords_in_four_directions(
                correct_coord
            ),
        )
        self.assertIn(
            {"row": "D", "column": 5},
            self.board.get_neighb_coords_in_four_directions(
                correct_coord
            ),
        )
        self.assertIn(
            {"row": "C", "column": 4},
            self.board.get_neighb_coords_in_four_directions(
                correct_coord
            ),
        )
        self.assertIn(
            {"row": "C", "column": 6},
            self.board.get_neighb_coords_in_four_directions(
                correct_coord
            ),
        )
        self.assertEqual(
            4,
            len(
                self.board.get_neighb_coords_in_four_directions(
                    correct_coord
                )
            ),
        )

        # Incorrect coords
        incorrect_coord_with_column_out_of_range = {"row": "J", "column": 11}
        self.assertRaises(
            TypeError,
            self.board.get_neighb_coords_in_four_directions,
            incorrect_coord_with_column_out_of_range,
        )

        incorrect_coord_with_row_out_of_range = {"row": "K", "column": 3}
        self.assertRaises(
            TypeError,
            self.board.get_neighb_coords_in_four_directions,
            incorrect_coord_with_row_out_of_range,
        )

    def test_get_neighb_coords_in_eight_directions(self):
        # coord of right down corner - should have only 3 neighb coords
        correct_coord_right_down_corner = {"row": "J", "column": 10}
        self.assertIn(
            {"row": "I", "column": 10},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_right_down_corner
            ),
        )
        self.assertIn(
            {"row": "J", "column": 9},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_right_down_corner
            ),
        )
        self.assertIn(
            {"row": "I", "column": 9},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_right_down_corner
            ),
        )
        self.assertEqual(
            3,
            len(
                self.board.get_neighb_coords_in_eight_directions(
                    correct_coord_right_down_corner
                )
            ),
        )

        # coord which should have 8 neighb coords
        correct_coord_middle = {"row": "E", "column": 5}
        self.assertIn(
            {"row": "E", "column": 4},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "E", "column": 6},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "D", "column": 4},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "D", "column": 5},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "D", "column": 6},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "F", "column": 4},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "F", "column": 5},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertIn(
            {"row": "F", "column": 6},
            self.board.get_neighb_coords_in_eight_directions(
                correct_coord_middle
            ),
        )
        self.assertEqual(
            8,
            len(
                self.board.get_neighb_coords_in_eight_directions(
                    correct_coord_middle
                )
            ),
        )

        # Incorrect coords
        incorrect_coord_with_column_out_of_range = {"row": "J", "column": 11}
        self.assertRaises(
            TypeError,
            self.board.get_neighb_coords_in_eight_directions,
            incorrect_coord_with_column_out_of_range,
        )

        incorrect_coord_with_row_out_of_range = {"row": "K", "column": 3}
        self.assertRaises(
            TypeError,
            self.board.get_neighb_coords_in_eight_directions,
            incorrect_coord_with_row_out_of_range,
        )

    def test_get_coord_from_coord_with_row_index(self):
        correct_coord_with_row_index = {"row_index": 1, "column": 10}
        coord = self.board.get_coord_from_coord_with_row_index(
            correct_coord_with_row_index
        )
        self.assertEqual({"row": "A", "column": 10}, coord)

        incorrect_coord_with_row_index_out_of_range = {
            "row_index": 11,
            "column": 10,
        }
        coord1 = self.board.get_coord_from_coord_with_row_index(
            incorrect_coord_with_row_index_out_of_range
        )
        self.assertIs(None, coord1)

        incorrect_coord_with_row_index_as_letter = {"row_index": "A", "column": 1}
        coord2 = self.board.get_coord_from_coord_with_row_index(
            incorrect_coord_with_row_index_as_letter
        )
        self.assertIs(None, coord2)

        incorrect_coord_with_column_as_letter = {"row_index": 4, "column": "B"}
        coord3 = self.board.get_coord_from_coord_with_row_index(
            incorrect_coord_with_column_as_letter
        )
        self.assertIs(None, coord3)

    def test_add_ship(self):
        ship_size_1 = Ship(row="A", column=1, size=1, orientation="horizontal")
        ship_size_2 = Ship(row="C", column=3, size=2, orientation="vertical")
        ship_size_3 = Ship(row="F", column=7, size=3, orientation="horizontal")
        ship_size_4 = Ship(row="A", column=10, size=4, orientation="vertical")

        self.assertTrue(self.board.add_ship(ship_size_1))
        self.assertTrue(self.board.add_ship(ship_size_2))
        self.assertTrue(self.board.add_ship(ship_size_3))
        self.assertTrue(self.board.add_ship(ship_size_4))

        ship_with_incorrect_coords_without_board = Ship(
            row="A", column=11, size=1, orientation="horizontal"
        )
        self.assertRaises(
            CustomException,
            self.board.add_ship,
            ship_with_incorrect_coords_without_board,
        )

        ship_with_incorrect_coords_too_close_another_ship = Ship(
            row="B", column=1, size=3, orientation="horizontal"
        )
        self.assertRaises(
            CustomException,
            self.board.add_ship,
            ship_with_incorrect_coords_too_close_another_ship,
        )


class TestDataUtils(unittest.TestCase):
    def setUp(self):
        self.data_utils = DataUtils()

    def test_serialize_to_json(self):
        dict_data = {"key1": "value1", "key2": "value2"}
        json_data = self.data_utils.serialize_to_json(dict_data)
        self.assertIsInstance(json_data, bytes)

    def test_deserialize_json(self):
        json_data = b'{"key1": "value1", "key2": "value2"}'
        dict_data = DataUtils.deserialize_json(json_data)
        self.assertIsInstance(dict_data, dict)
        self.assertEqual(dict_data, {"key1": "value1", "key2": "value2"})


class TestDatabaseUtils(unittest.TestCase):
    def setUp(self):
        self.database_utils = DatabaseUtils(test_db_file)
        self.database_utils.create_game_table()
        self.database_utils.create_board_table("test_boards")
        self.connection = self.database_utils.create_connection()
        self.delete_games_query = "DELETE FROM games"
        self.delete_boards_query = "DELETE FROM test_boards"

    def tearDown(self):
        self.connection.close()

    def test_create_game_table(self):
        query = (
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'games';"
        )
        result = self.database_utils.execute_sql_query(query, fetch_option="fetchone")
        self.assertIsNotNone(result)

    def test_create_board_table(self):
        query = f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'test_boards';"
        result = self.database_utils.execute_sql_query(query, fetch_option="fetchone")
        self.assertIsNotNone(result)

    def test_add_game_to_db(self):
        self.database_utils.execute_sql_query(self.delete_games_query)
        for _ in range(5):
            self.database_utils.add_game_to_db()
        games = self.database_utils.get_all_games()
        self.assertIsNotNone(games)
        self.assertEqual(5, len(games))

    def test_delete_games_with_non_finite_status(self):
        self.database_utils.delete_boards_for_game_with_non_finite_status(
            board_table="games"
        )
        query = "SELECT * FROM games WHERE winner is NULL"
        result = self.database_utils.execute_sql_query(query)
        self.assertIsNone(result)

    def test_set_winner(self):
        self.database_utils.add_game_to_db()
        self.database_utils.set_winner(1, "TEST_WINNER")
        result_query = "SELECT winner FROM games WHERE game_id = ?"
        result = self.database_utils.execute_sql_query(
            result_query, "1", fetch_option="fetchone"
        )
        self.assertIsNotNone(result)
        self.assertEqual("TEST_WINNER", result[0])
        self.database_utils.execute_sql_query(self.delete_games_query)

    def test_add_board_to_db(self):
        board_status = {
            "A": {
                "1": "~",
                "2": "~",
                "3": "~",
                "4": "~",
                "5": "~",
                "6": "~",
                "7": "~",
                "8": "~",
                "9": "~",
                "10": "~",
            }
        }
        self.database_utils.add_game_to_db()
        self.database_utils.add_board_to_db(1, board_status, "test_boards")
        board_query = "SELECT board_status FROM test_boards WHERE game_id = ?"
        result = self.database_utils.execute_sql_query(
            board_query, "1", fetch_option="fetchone"
        )
        self.assertIsNotNone(result)
        self.assertEqual(board_status, json.loads(result[0]))
        self.database_utils.execute_sql_query(self.delete_boards_query)
        self.database_utils.execute_sql_query(self.delete_games_query)
