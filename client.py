import socket
from data_utils import DataUtils
from communication_utils import CommunicationUtilsClient
from config_variables import HOST, PORT, BUFFER, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, db_file
from player import Player, AIPlayer


class Client:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.buffer = BUFFER
        self.internet_address_family = INTERNET_ADDRESS_FAMILY
        self.socket_type = SOCKET_TYPE
        self.data_utils = DataUtils()
        self.player = Player()
        self.ai_player = AIPlayer()
        self.communication_utils = CommunicationUtilsClient(self.player)
        self.is_running = True

    def create_request_to_server(self, client_input, args=None):
        if client_input == "START":
            return self.communication_utils.client_game_invitation_request()
        elif client_input == "SHOT":
            return self.communication_utils.client_shot_request()
        elif client_input == "SHOT_REQUEST":
            return self.communication_utils.client_requesting_server_to_shot()
        elif client_input == "BOARD":
            return self.communication_utils.client_send_final_ships_positions()
        elif client_input == "SAVE_GAME_TO_DB":
            return self.communication_utils.client_request_to_db_service("SAVE_GAME_TO_DB")
        elif client_input == "SAVE_BOARD_STATUS_TO_DB":
            return self.communication_utils.client_request_to_db_service("SAVE_BOARD_STATUS_TO_DB", {"player_board": self.player.player_board,
                                                                                                     "opponent_board": self.ai_player.player_board})
        elif client_input == "SAVE_WINNER_TO_DB":
            return self.communication_utils.client_request_to_db_service("SAVE_WINNER_TO_DB", {"winner": args})
        elif client_input == "SHOW_ARCHIVED_GAMES":
            return self.communication_utils.client_request_to_db_service("SHOW_ARCHIVED_GAMES")
        elif client_input == "STOP":
            return self.communication_utils.stop_client_and_server()
        else:
            return self.communication_utils.client_send_unknown_command()

    def read_server_response(self, server_response_json, client_socket):
        server_response = self.data_utils.deserialize_json(server_response_json)
        if server_response['type'] == "SHOT_REQUEST":
            client_response = self.communication_utils.client_response_for_server_shot(server_response)
            client_response_json = self.data_utils.serialize_to_json(client_response)
            client_socket.sendall(client_response_json)
            server_response_json = client_socket.recv(self.buffer)
            server_response = self.data_utils.deserialize_json(server_response_json)
            return server_response
        if server_response['type'] == "SHOT" and server_response['status'] == "OK":
            result = server_response["body"]
            self.player.player_board.add_result_of_player_shot_into_opponent_board(self.communication_utils.last_shot,
                                                                                   result)
            return result
        if server_response['type'] == "GAME_INVITATION" and server_response['status'] == 'OK':
            self.player.aut_coordinates_for_ship_add_to_board()
            self.player.player_board.prepare_board_for_game_start()
        return server_response

    def automation_game(self, client_socket):
        turn = 1
        while True:
            print(f">>>>>>>>>>TURN: {turn}<<<<<<<<<<")
            self.player.player_board.reload_boards()
            self.communication_feature_template(client_socket, "SAVE_BOARD_STATUS_TO_DB")
            client_shot = self.communication_feature_template(client_socket, "SHOT")
            print(client_shot)
            number_of_sunk_signs_in_player_opponent_board = self.player.player_board.count_sunk_signs()
            if number_of_sunk_signs_in_player_opponent_board == 20:
                winner = "CLIENT"
                break
            self.repeat_shot_check(client_shot, client_socket, "SHOT")
            number_of_sunk_signs_in_player_opponent_board_2 = self.player.player_board.count_sunk_signs()
            if number_of_sunk_signs_in_player_opponent_board_2 == 20:
                winner = "CLIENT"
                break
            server_shot = self.communication_feature_template(client_socket, "SHOT_REQUEST")
            print(server_shot)
            number_of_sunk_signs_in_ai_player_opponent_board = self.ai_player.player_board.count_sunk_signs()
            if number_of_sunk_signs_in_ai_player_opponent_board == 20:
                winner= "SERVER"
                break
            self.repeat_shot_check(server_shot, client_socket, "SHOT_REQUEST")
            number_of_sunk_signs_in_ai_player_opponent_board_2 = self.ai_player.player_board.count_sunk_signs()
            if number_of_sunk_signs_in_ai_player_opponent_board_2 == 20:
                winner = "SERVER!"
                break
            turn += 1
        winner_message = self.communication_feature_template(client_socket, "SAVE_WINNER_TO_DB", winner)
        print(winner_message["body"])


    def check_server_response_instance(self, server_response):
        if isinstance(server_response, str):
            return server_response
        elif isinstance(server_response, dict):
            return server_response["body"]

    def repeat_shot_check(self, server_response_object, client_socket, shot):
        check_server_response = self.check_server_response_instance(server_response_object)
        if check_server_response in ["HIT", "SINKING"]:
            shot_repeat = True
            while shot_repeat:
                number_of_sunk_signs_in_player_opponent_board = self.player.player_board.count_sunk_signs()
                number_of_sunk_signs_in_ai_player_opponent_board = self.ai_player.player_board.count_sunk_signs()
                if number_of_sunk_signs_in_player_opponent_board == 20 or number_of_sunk_signs_in_ai_player_opponent_board == 20:
                    break
                self.player.player_board.reload_boards()
                shot_response = self.communication_feature_template(client_socket, shot)
                if shot_response not in ["HIT", "SINKING"]:
                    shot_repeat = False

    def communication_feature_template(self, client_socket, request, args=None):
        client_request = self.create_request_to_server(request, args)
        client_request_json = self.data_utils.serialize_to_json(client_request)
        client_socket.sendall(client_request_json)
        server_response_json = client_socket.recv(self.buffer)
        server_response = self.read_server_response(server_response_json, client_socket)
        return server_response

    def start(self):
        with socket.socket(self.internet_address_family, self.socket_type) as client_socket:
            client_socket.connect((self.host, self.port))
            while self.is_running:
                print(
                    "Type:\n'Start' for starting the game\n'Show' for showing archived games\n'Stop' for stopping the application")
                client_input = input("Request: ").upper()
                if client_input == "STOP":
                    self.stop(client_socket, client_input)
                else:
                    client_request = self.create_request_to_server(client_input)
                    client_request_json = self.data_utils.serialize_to_json(client_request)
                    client_socket.sendall(client_request_json)
                    server_response_json = client_socket.recv(self.buffer)
                    self.read_server_response(server_response_json, client_socket)
                    if client_input == "START":
                        self.communication_feature_template(client_socket, "SAVE_GAME_TO_DB")
                        self.automation_game(client_socket)
                    elif client_input == "SHOW":
                        server_response = self.communication_feature_template(client_socket, "SHOW_ARCHIVED_GAMES")
                        all_games = server_response["body"]
                        if all_games == None or all_games == []:
                            print("There`s no game to watch")
                        else:
                            for game in all_games:
                                print(game)
                            game_id = input("Which game do you want to watch ? Give her ID: ")
                            try:
                                pass
                            except ValueError as e:
                                print(e)

    def stop(self, client_socket, client_input):
        client_request = self.create_request_to_server(client_input)
        client_request_json = self.data_utils.serialize_to_json(client_request)
        client_socket.sendall(client_request_json)
        print("Client's shutting down...")
        self.is_running = False


if __name__ == "__main__":
    client = Client()
    client.start()
