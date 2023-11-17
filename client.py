import socket
from data_utils import DataUtils
from communication_utils import CommunicationUtilsClient
from config_variables import HOST, PORT, BUFFER, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE
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

    def create_request_to_server(self, client_input):
        if client_input == "START":
            return self.communication_utils.client_game_invitation_request()
        elif client_input == "SHOT":
            return self.communication_utils.client_shot_request()
        elif client_input == "SHOT_REQUEST":
            return self.communication_utils.client_requesting_server_to_shot()
        elif client_input == "BOARD":
            return self.communication_utils.client_send_final_ships_positions()
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
            row_from_last_shot = self.communication_utils.last_shot["row"]
            column_from_last_shot = self.communication_utils.last_shot["column"]
            result = server_response["body"]
            self.player.player_board.add_result_of_player_shot_into_opponent_board(row_from_last_shot,
                                                                                   column_from_last_shot, result)
            return result
        if server_response['type'] == "GAME_INVITATION" and server_response['status'] == 'OK':
            self.player.coordinates_for_ship_add_to_board()
            self.player.player_board.prepare_board_for_game_start()
        return server_response

    def automation_game(self, client_socket):
        turn = 1
        while True:
            print(f">>>>>>>>>>TURN: {turn}<<<<<<<<<<")
            number_of_sunk_signs_in_player_board = self.player.player_board.count_sunk_signs()
            number_of_sunk_signs_in_ai_player_board = self.ai_player.player_board.count_sunk_signs()
            if number_of_sunk_signs_in_player_board == 20 or number_of_sunk_signs_in_ai_player_board == 20:
                break
            self.player.player_board.reload_boards()
            client_shot = self.create_request_to_server("SHOT")
            client_shot_json = self.data_utils.serialize_to_json(client_shot)
            client_socket.sendall(client_shot_json)
            server_response_for_client_shot_json = client_socket.recv(self.buffer)
            server_response_for_client_shot = self.read_server_response(server_response_for_client_shot_json, client_socket)
            print(server_response_for_client_shot)
            self.repeat_shot_check(server_response_for_client_shot, client_socket, "SHOT")
            server_shot = self.create_request_to_server("SHOT_REQUEST")
            server_shot_json = self.data_utils.serialize_to_json(server_shot)
            client_socket.sendall(server_shot_json)
            server_response_for_own_shot_json = client_socket.recv(self.buffer)
            server_response_for_own_shot = self.read_server_response(server_response_for_own_shot_json, client_socket)
            print(server_response_for_own_shot_json)
            self.repeat_shot_check(server_response_for_own_shot, client_socket, "SHOT_REQUEST")
            turn += 1

    def check_server_response_instance(self, server_response):
        if isinstance(server_response, str):
            return server_response
        elif isinstance(server_response, dict):
            return server_response["body"]

    def repeat_shot_check(self, server_response_obj, client_socket, shot):
        server_response = self.check_server_response_instance(server_response_obj)
        if server_response in ["HIT", "SINKING"]:
            shot_repeat = True
            while shot_repeat:
                self.player.player_board.reload_boards()
                shot = self.create_request_to_server(shot)
                shot_json = self.data_utils.serialize_to_json(shot)
                client_socket.sendall(shot_json)
                shot_response_json = client_socket.recv(self.buffer)
                shot_response = self.read_server_response(shot_response_json, client_socket)
                if shot_response not in ["HIT", "SINKING"]:
                    shot_repeat = False

    def start(self):
        with socket.socket(self.internet_address_family, self.socket_type) as client_socket:
            client_socket.connect((self.host, self.port))
            while self.is_running:
                print("Type: \n'Start' for start the game \n'Show' for show archived games \n'Stop for stop application")
                client_input = input("Request: ").upper()
                if client_input == "STOP":
                    self.stop(client_socket, client_input)
                client_request = self.create_request_to_server(client_input)
                client_request_json = self.data_utils.serialize_to_json(client_request)
                client_socket.sendall(client_request_json)
                server_response_json = client_socket.recv(self.buffer)
                self.read_server_response(server_response_json, client_socket)
                self.automation_game(client_socket)

    def stop(self, client_socket, client_input):
        client_request = self.create_request_to_server(client_input)
        client_request_json = self.data_utils.serialize_to_json(client_request)
        client_socket.sendall(client_request_json)
        print("Client`s shutting down...")
        self.is_running = False
        client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.start()
