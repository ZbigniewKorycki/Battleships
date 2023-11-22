import json
import sqlite3
from sqlite3 import Error


class DataUtils:

    def __init__(self):
        self.encode_format = "UTF-8"

    def serialize_to_json(self, data):
        return json.dumps(data).encode(self.encode_format)

    def deserialize_json(self, data):
        return json.loads(data)

    def board_json_serialize(self, board_status):
        return json.dumps(board_status)


class DatabaseUtils:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_game_table()
        self.create_board_table("client_boards")
        self.create_board_table("server_boards")
        self.data_utils = DataUtils()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option=None):
        connection = self.create_connection()
        cursor = connection.cursor()
        if connection is not None:
            try:
                cursor.execute(query, *args)
                connection.commit()
                if fetch_option == "fetchone":
                    return cursor.fetchone()
                elif fetch_option == "fetchall":
                    return cursor.fetchall()
            except Error as e:
                print(f"Error: {e}")
                connection.rollback()
            finally:
                cursor.close()
                connection.close()
        else:
            print("Cannot create the database connection.")

    def create_game_table(self):
        create_games_table_query = """ CREATE TABLE IF NOT EXISTS games(
                                      game_id INTEGER PRIMARY KEY,
                                      game_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      winner VARCHAR NOT NULL DEFAULT 'the game has not been completed'
                                      ); """
        self.execute_sql_query(create_games_table_query)

    def create_board_table(self, board_owner):
        create_boards_table_query = f""" CREATE TABLE IF NOT EXISTS {board_owner}(
                                       board_id INTEGER PRIMARY KEY,
                                       game_id INTEGER NOT NULL,
                                       board_status TEXT NOT NULL,
                                       FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE CASCADE
                                       ); """
        self.execute_sql_query(create_boards_table_query)

    def add_game_to_db(self):
        query = "INSERT INTO games " \
                "DEFAULT VALUES"
        self.execute_sql_query(query)

    def add_board_to_db(self, game_number, board_status, board_table):
        game_id_query = "SELECT game_id FROM games " \
                        "WHERE game_id = ?"
        game_id = self.execute_sql_query(game_id_query, (game_number,), fetch_option="fetchone")[0]
        board_status_json = self.data_utils.board_json_serialize(board_status)
        query = f"INSERT INTO {board_table} (game_id, board_status)" \
                "VALUES (?, ?)"
        self.execute_sql_query(query, (game_id, board_status_json))

    def get_all_games(self):
        query = "SELECT * FROM games " \
                "ORDER BY game_id"
        all_games = self.execute_sql_query(query, fetch_option="fetchall")
        return all_games

    def delete_games_with_non_finite_status(self):
        query = "DELETE FROM games " \
                "WHERE winner = 'the game has not been completed'"
        self.execute_sql_query(query)

    def set_winner(self, game_number, winner):
        query = "UPDATE games " \
                "SET winner = ? " \
                "WHERE game_id = ?"
        self.execute_sql_query(query, (winner, game_number))
