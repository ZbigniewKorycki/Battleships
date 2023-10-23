import random
import string


class CommunicationUtils:

    def __init__(self):
        self.server_busy = False
        self.null_value = "null"
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
        self.row_index = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7,
            "I": 8,
            "J": 9
        }
        self.shot_possibilities = {
            0: "MISS",
            1: "HIT",
            2: "SINKING"
        }

    def protocol_template(self, message_type, status, message, body):
        template = {
            "type": message_type,
            "status": status,
            "message": message,
            "body": body
        }
        return template

    def game_invitation_request(self):
        client_request = self.protocol_template(self.message_type[0], self.status_code[0], self.null_value,
                                                self.null_value)
        return client_request

    def game_invitation_response(self):
        if self.server_busy == False:
            server_response = self.protocol_template(self.message_type[0], self.status_code[1],
                                                     "Server is playing the other game", self.null_value)
        else:
            server_response = self.protocol_template(self.message_type[0], self.status_code[0], self.null_value,
                                                     self.null_value)
        return server_response

    def client_shot_request(self):
        row_input = input("CHOOSE ROW FROM 'A' TO 'J': ").capitalize()
        column_input = input("CHOOSE COLUMN FROM '1' TO '10': ")
        body_template = {
            "row": row_input,
            "column": int(column_input)
        }
        client_shot = self.protocol_template(self.message_type[1], self.status_code[0], self.null_value, body_template)
        return client_shot

    def client_shot_result(self, client_shot_request):
        co_ordinates = client_shot_request["body"]
        row = co_ordinates["row"]
        row_index = self.row_index[row]
        column_index = co_ordinates["column"]
        shot_success = self.protocol_template(self.message_type[1], self.status_code[0], self.null_value,
                                              self.shot_possibilities[1])
        shot_missed = self.protocol_template(self.message_type[1], self.status_code[0], self.null_value,
                                             self.shot_possibilities[0])
        ship_destroy = self.protocol_template(self.message_type[1], self.status_code[0], self.null_value,
                                              self.shot_possibilities[2])
        if row_index < 0 or row_index > 9 or column_index < 1 or column_index > 10:
            error_message = self.protocol_template(self.message_type[1], self.status_code[2],
                                                   "The shot is not within the boundaries of the board",
                                                   self.null_value)
            return error_message
        else:
            result_message = self.protocol_template(self.message_type[1], self.status_code[0],
                                                    "The shot within the boundaries of the board",
                                                    body="HIT/MISS/SINKING")
            return result_message

    def server_shot_request(self):
        shot_request = self.protocol_template(self.message_type[2], self.null_value, self.null_value, self.null_value)
        return shot_request

    def server_shot(self):
        row = random.randint(1, 10)
        column = random.randint(1, 10)
        row_letter = string.ascii_uppercase[row]
        body_template = {
            "row": row_letter,
            "column": column
        }
        server_shot_message = self.protocol_template(self.message_type[2], self.status_code[0], self.null_value,
                                                     body_template)
        return server_shot_message

    def server_shot_result(self, server_shot_request):
        co_ordinates = server_shot_request["body"]
        row = co_ordinates["row"]
        row_index = self.row_index[row]
        column_index = co_ordinates["column"]
        shot_success = self.protocol_template(self.message_type[3], self.null_value, self.null_value,
                                              self.shot_possibilities[1])
        shot_missed = self.protocol_template(self.message_type[3], self.null_value, self.null_value,
                                             self.shot_possibilities[0])
        ship_destroy = self.protocol_template(self.message_type[3], self.null_value, self.null_value,
                                              self.shot_possibilities[2])
        return {"type": "RESULT", "body": "HIT/MISS/SINKING"}

    def server_shot_response(self):
        server_response = self.protocol_template(self.message_type[3], self.status_code[0], self.null_value,
                                                 self.null_value)
        return server_response

    def unknown_command(self):
        unknown_command_message = self.protocol_template(self.message_type[5], self.status_code[4], self.null_value,
                                                         self.null_value)
        return unknown_command_message

    def ships_positions(self):
        ships_position_message = {"type": "BOARD",
                                  "body": {
                                      "four": "B3-B6",
                                      "three": ["E10-G10", "F3-H3"],
                                      "two": ["A9-B9", "D7-D8", "I6-I7"],
                                      "one": ["D2", "D5", "F7", "I9"]
                                  }
                                  }
        return ships_position_message

    def ships_positions_server_confirmation(self):
        confirmation = self.protocol_template(self.message_type[4], self.status_code[0], self.null_value,
                                              self.null_value)
        return confirmation
