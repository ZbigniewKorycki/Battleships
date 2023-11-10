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


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_db_tables()

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
                                      game_date DATE NOT NULL DEFAULT CURRENT_DATE
                                      ); """
        self.execute_sql_query(create_game_table_query)

    def create_board_table(self, table_name, board_number):
        create_board_table_query = f""" CREATE TABLE IF NOT EXISTS {table_name}(
                                         {board_number}_board_id INTEGER PRIMARY KEY,
                                         game_id INTEGER NOT NULL,
                                         board_status TEXT NOT NULL,
                                         FOREIGN KEY (game_id) REFERENCES games (game_id) ON DELETE CASCADE
                                         ); """
        self.execute_sql_query(create_board_table_query)

    def create_db_tables(self):
        self.create_game_table()
        self.create_board_table("first_boards", "first")
        self.create_board_table("second_boards", "second")
        self.create_board_table("third_boards", "third")
        self.create_board_table("fourth_boards", "fourth")

