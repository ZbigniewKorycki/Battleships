from data_utils import DatabaseUtils
from config_variables import db_file


class CommunicationUtils:

    def __init__(self):
        self.server_is_busy = False
        self.last_shot = None
        self.message_type = {
            0: "GAME_INVITATION",
            1: "SHOT",
            2: "SHOT_REQUEST",
            3: "RESULT",
            4: "BOARD",
            5: "UNKNOWN"
        }
        self.status_code = {
            0: "OK",
            1: "SEVER_BUSY",
            2: "ILLEGAL_ARGUMENTS",
            3: "INTERNAL_ERROR",
            4: "BAD_REQUEST"
        }
        self.shot_result = {
            0: "MISS",
            1: "HIT",
            2: "SINKING"
        }

    def protocol_template(self, message_type="null", status="null", message="null", body="null"):
        template = {
            "type": message_type,
            "status": status,
            "message": message,
            "body": body
        }
        return template


class CommunicationUtilsClient(CommunicationUtils):
    def __init__(self, player_client):
        super().__init__()
        self.player_client = player_client

    def protocol_template(self, message_type="null", body='null', *args):
        template = {
            "type": message_type,
            "body": body
        }
        return template

    def client_game_invitation_request(self):
        client_request = self.protocol_template(self.message_type[0])
        return client_request

    def client_shot_request(self):
        counter_max_tries = 2
        while counter_max_tries > 0:
            row_input = input("CHOOSE ROW FROM 'A' TO 'J': ").capitalize()
            column_input = input("CHOOSE COLUMN FROM '1' TO '10': ")
            if not self.verify_client_shot_request(row_input, column_input):
                counter_max_tries -= 1
                if counter_max_tries == 1:
                    print(f"Incorrect coordinates, you have last chance to give correct, row: (A-J) column: (1-10).")
            else:
                message_shot_request = {
                    "row": row_input,
                    "column": int(column_input)
                }
                client_shot = self.protocol_template(self.message_type[1], message_shot_request)
                self.last_shot = message_shot_request
                return client_shot
        message_invalid_shot_request = {
            "row": 'INVALID',
            "column": 1
        }
        client_invalid_shot = self.protocol_template(self.message_type[1], message_invalid_shot_request)
        self.last_shot = message_invalid_shot_request
        return client_invalid_shot

    def verify_client_shot_request(self, row, column):
        # row should be string, column integer
        try:
            int(row)
        except ValueError:
            try:
                int(column)
            except ValueError:
                return False
            else:
                return True
        else:
            return False

    def client_requesting_server_to_shot(self):
        shot_request = self.protocol_template(self.message_type[2])
        return shot_request

    def client_response_for_server_shot(self, server_shot_request):
        coordinate = server_shot_request["body"]
        shot_result = self.player_client.player_board.result_of_opponent_shot(coordinate)
        if shot_result == "MISS" or shot_result == "HIT" or shot_result == "SINKING":
            return self.protocol_template(self.message_type[3], body=shot_result)
        else:
            return self.protocol_template(self.message_type[3], body='MISS')

    def client_send_final_ships_positions(self):
        final_ships_positions = self.player_client.player_board.get_positions_of_all_ships()
        message_with_final_ships_positions = self.protocol_template(self.message_type[4], final_ships_positions)
        return message_with_final_ships_positions

    def client_send_unknown_command(self):
        message_unknown_command = self.protocol_template(self.message_type[5])
        return message_unknown_command

    def client_request_to_db_service(self, request, args=None):
        if request == "SAVE_GAME_TO_DB":
            client_request = self.protocol_template(message_type="SAVE_GAME")
        elif request == "SAVE_BOARD_STATUS_TO_DB":
            client_request = self.protocol_template(message_type="SAVE_BOARD_STATUS", body=args)
        elif request == "SAVE_WINNER_TO_DB":
            client_request = self.protocol_template(message_type="SAVE_WINNER", body=args)
        elif request == "SHOW_ARCHIVED_GAMES":
            client_request = self.protocol_template(message_type="ARCHIVED_GAMES")
        return client_request

    def stop_client_and_server(self):
        stop_request = "STOP"
        return stop_request


class CommunicationUtilsServer(CommunicationUtils):
    def __init__(self, player_server):
        super().__init__()
        self.player_server = player_server

    def server_game_invitation_response(self):
        if self.server_is_busy:
            server_response = self.protocol_template(self.message_type[0], self.status_code[1],
                                                     "Server is playing the other game")
        else:
            server_response = self.protocol_template(self.message_type[0], self.status_code[0])
            self.server_is_busy = True
        return server_response

    def server_response_for_client_shot(self, client_shot_request):
        coordinate = client_shot_request["body"]
        shot_result = self.player_server.player_board.result_of_opponent_shot(coordinate)
        if shot_result == "MISS" or shot_result == "HIT" or shot_result == "SINKING":
            return self.protocol_template(self.message_type[1], self.status_code[0],
                                          body=shot_result)
        else:
            return self.protocol_template(self.message_type[1], self.status_code[2],
                                          "The shot within the boundaries of the board")

    def server_shot(self):
        row, column = self.player_server.ai_shot()
        shot_message = {"row": row,
                        "column": column}
        self.last_shot = shot_message
        server_shot_message = self.protocol_template(self.message_type[2], self.status_code[0], body=shot_message)
        return server_shot_message

    def server_acknowledgment_to_client_response_for_server_shot(self, result):
        if result == "MISS":
            server_response = self.protocol_template(self.message_type[3], self.status_code[0],
                                                     body=self.shot_result[0])
        elif result == "HIT":
            server_response = self.protocol_template(self.message_type[3], self.status_code[0],
                                                     body=self.shot_result[1])
        elif result == "SINKING":
            server_response = self.protocol_template(self.message_type[3], self.status_code[0],
                                                     body=self.shot_result[2])
        else:
            server_response = self.protocol_template(self.message_type[3], self.status_code[0])
        return server_response

    def server_response_to_unknown_command(self):
        unknown_command_message = self.protocol_template(self.message_type[5], self.status_code[4])
        return unknown_command_message

    def server_confirmation_to_final_ships_positions(self):
        confirmation = self.protocol_template(self.message_type[4], self.status_code[0])
        return confirmation


class DatabaseCommunicationUtils(CommunicationUtils):
    def __init__(self):
        super().__init__()
        self.database_utils = DatabaseUtils(db_file)

    def save_game_to_db(self):
        self.database_utils.add_game_to_db()
        response = self.protocol_template(message_type="SAVE_GAME", body="The game was successfully added to database")
        return response

    def save_board_to_db(self, player_board, opponent_board):
        game_number = self.establish_game_number()
        self.database_utils.add_board_to_db(game_number, player_board, "client_boards")
        self.database_utils.add_board_to_db(game_number, opponent_board, "server_boards")
        response = self.protocol_template(message_type="SAVE_BOARDS", body="Boards was successfully added to database")
        return response

    def set_winner_in_table(self, winner):
        game_number = self.establish_game_number()
        self.database_utils.set_winner(game_number, winner)
        response = self.protocol_template(message_type="SAVE_WINNER", body=f"{winner} WINS !")
        return response

    def delete_games_without_winner(self):
        return self.database_utils.delete_games_with_non_finite_status()

    def show_all_games(self):
        all_games = self.database_utils.get_all_games()
        response = self.protocol_template(message_type="ARCHIVED_GAMES", body=all_games)
        return response

    def establish_game_number(self):
        number_of_games_in_the_database = self.database_utils.get_all_games()
        actually_game_number = number_of_games_in_the_database[-1]
        return actually_game_number

