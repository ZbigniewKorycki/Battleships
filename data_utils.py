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


class DatabaseUtils:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_game_table()
        self.create_board_table()

    def create_connection(self):
        try:
            connection = sqlite3.connect(self.db_file)
            return connection
        except Error as e:
            print(f"Error: {e}")
            return None

    def execute_sql_query(self, query, *args, fetch_option = None):
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
        create_game_table_query = """ CREATE TABLE IF NOT EXISTS games(
                                      game_id INTEGER PRIMARY KEY,
                                      game_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                      winner VARCHAR NOT NULL DEFAULT 'the game has not been completed'
                                      ); """
        self.execute_sql_query(create_game_table_query)

    def create_board_table(self):
        create_board_table_query = """ CREATE TABLE IF NOT EXISTS boards(
                                       board_id INTEGER PRIMARY KEY,
                                       game_id INTEGER NOT NULL,
                                       board_status TEXT NOT NULL,
                                       board_number_in_order INTEGER NOT NULL,
                                       FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE CASCADE
                                       ); """
        self.execute_sql_query(create_board_table_query)

    def add_game_to_db(self, game_datetime):
        query = "INSERT INTO games (game_datetime) " \
                "VALUES (?)"
        self.execute_sql_query(query, (game_datetime, ))

    def add_board_to_db(self, game_number, board, board_number):
        # The first board represents the server's original ship placement along with marked client shots.
        # The second board displays the server's shots, including marked hits.
        # The third board shows the client's original ship placement with marked server shots.
        # The fourth board illustrates the client's shots, including marked hits.
        board_json_serialize = json.dumps(board)
        game_id_query = "SELECT game_id FROM games " \
                        "WHERE game_id = ?"
        game_id = self.execute_sql_query(game_id_query, (game_number, ), fetch_option = "fetchone")[0]
        query = "INSERT INTO boards (game_id, board_status, board_number)" \
                "VALUES (?, ?, ?)"
        self.execute_sql_query(query, (game_id, board_json_serialize, board_number))

    def get_all_games(self):
        query = "SELECT * FROM games"
        all_games = self.execute_sql_query(query, fetch_option = "fetchall")
        return all_games

    def get_boards_status_for_game(self, game_number):
        query = "SELECT board_status FROM boards " \
                "WHERE game_id = (SELECT game_id FROM games WHERE game_id = ?) " \
                "ORDER BY board_number_in_order"
        boards = self.execute_sql_query(query, (game_number, ), fetch_option = "fetchall")
        return boards

    def set_winner(self, winner_message, game_number):
        if winner_message == "YOU WIN !":
            winner = "CLIENT"
        elif winner_message == "ENEMY WINS !":
            winner = "SERVER"
        query = "UPDATE games " \
                "SET winner = ? " \
                "WHERE game_id = ?"
        self.execute_sql_query(query, (winner, game_number))


