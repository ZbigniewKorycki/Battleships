import socket
from data_utils import DataUtils
from communication_utils import CommunicationUtilsServer
from config_variables import HOST, PORT, BUFFER, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE
from player import AIPlayer


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.buffer = BUFFER
        self.internet_address_family = INTERNET_ADDRESS_FAMILY
        self.socket_type = SOCKET_TYPE
        self.data_utils = DataUtils()
        self.ai_player = AIPlayer()
        self.communication_utils = CommunicationUtilsServer(self.ai_player)
        self.is_running = True

    def read_client_request(self, client_request_json):
        return self.data_utils.deserialize_json(client_request_json)

    def create_response_to_client(self, client_request):
        if client_request['type'] == 'GAME_INVITATION':
            response_for_game_invitation = self.communication_utils.server_game_invitation_response()
            if response_for_game_invitation["status"] == 'OK':
                self.ai_player.coordinates_for_ship_add_to_board()
                self.ai_player.player_board.prepare_board_for_game_start()
            return response_for_game_invitation
        elif client_request['type'] == 'SHOT':
            return self.communication_utils.server_response_for_client_shot(client_request)
        elif client_request['type'] == 'SHOT_REQUEST':
            return self.communication_utils.server_shot()
        elif client_request['type'] == 'BOARD':
            return self.communication_utils.server_confirmation_to_final_ships_positions()
        elif client_request['type'] == 'RESULT':
            result = client_request["body"]
            self.ai_player.player_board.add_result_of_player_shot_into_opponent_board(self.communication_utils.last_shot, result)
            return self.communication_utils.server_acknowledgment_to_client_response_for_server_shot(result)
        else:
            return self.communication_utils.server_response_to_unknown_command()

    def start(self):
        with socket.socket(self.internet_address_family, self.socket_type) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            while self.is_running:
                client_request_json = client_socket.recv(self.buffer)
                client_request = self.read_client_request(client_request_json)
                print(client_request)
                if client_request == "STOP":
                    self.stop(server_socket)
                else:
                    response_to_client = self.create_response_to_client(client_request)
                    response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
                    client_socket.sendall(response_to_client_json)
                    self.ai_player.player_board.reload_boards()

    def stop(self, server_socket):
        print("Server`s shutting down...")
        self.is_running = False
        server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start()
