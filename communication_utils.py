import random


class CommunicationUtils:

    def __init__(self):
        self.server_is_busy = False
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

    def protocol_template(self, message_type="null", status="null", message="null", body='null'):
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
        row_input = input("CHOOSE ROW FROM 'A' TO 'J': ").capitalize()
        column_input = input("CHOOSE COLUMN FROM '1' TO '10': ")
        body_template = {
            "row": row_input,
            "column": int(column_input)
        }
        client_shot = self.protocol_template(self.message_type[1], body=str(body_template))
        return client_shot

    def client_requesting_server_to_shot(self):
        shot_request = self.protocol_template(self.message_type[2])
        return shot_request

    def client_response_for_server_shot(self, server_shot_request):
        coordinates = server_shot_request["body"]
        row = coordinates["row"]
        column = coordinates["column"]
        shot_result = self.player_client.player_board.result_of_opponent_shot(row, column)
        if shot_result == "MISS" or shot_result == "HIT" or shot_result == "SINKING":
            return self.protocol_template(self.message_type[3], body=shot_result)
        else:
            return self.protocol_template(self.message_type[3], body='MISS')

    def client_send_final_ships_positions(self):
        ships_position_message = {"type": "BOARD",
                                  "body": {
                                      "four": "B3-B6",
                                      "three": ["E10-G10", "F3-H3"],
                                      "two": ["A9-B9", "D7-D8", "I6-I7"],
                                      "one": ["D2", "D5", "F7", "I9"]
                                  }
                                  }
        return ships_position_message


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
        return server_response

    def server_response_for_client_shot(self, client_shot_request):
        coordinates = client_shot_request["body"]
        row = coordinates["row"]
        column = coordinates["column"]
        shot_result = self.player_server.player_board.result_of_opponent_shot(row, column)
        if shot_result == "MISS" or shot_result == "HIT" or shot_result == "SINKING":
            return self.protocol_template(self.message_type[1], self.status_code[0],
                                          body=shot_result)
        else:
            return self.protocol_template(self.message_type[1], self.status_code[2],
                                          "The shot within the boundaries of the board")

    def server_shot(self):
        row = self.player_server.player_board.get_row_from_index(random.randint(1, 10))
        column = random.randint(1, 10)
        body_template = {
            "row": row,
            "column": column
        }
        server_shot_message = self.protocol_template(self.message_type[2], self.status_code[0], body=str(body_template))
        return server_shot_message

    def server_acknowledgment_to_client_response_for_server_shot(self):
        server_response = self.protocol_template(self.message_type[3], self.status_code[0])
        return server_response

    def server_response_to_unknown_command(self):
        unknown_command_message = self.protocol_template(self.message_type[5], self.status_code[4])
        return unknown_command_message

    def server_confirmation_to_final_ships_positions(self):
        confirmation = self.protocol_template(self.message_type[4], self.status_code[0])
        return confirmation
