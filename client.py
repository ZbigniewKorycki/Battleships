import socket
from data_utils import DataUtils
from communication_utils import CommunicationUtilsClient
from config_variables import HOST, PORT, BUFFER, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE
from player import Player


class Client:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.buffer = BUFFER
        self.internet_address_family = INTERNET_ADDRESS_FAMILY
        self.socket_type = SOCKET_TYPE
        self.data_utils = DataUtils()
        self.player = Player()
        self.communication_utils = CommunicationUtilsClient(self.player)
        self.is_running = True


    def create_request_to_server(self, client_input):
        if client_input == "GAME_INVITATION":
            return self.communication_utils.client_game_invitation_request()
        elif client_input == "SHOT":
            return self.communication_utils.client_shot_request()
        elif client_input == "SHOT_REQUEST":
            return self.communication_utils.client_requesting_server_to_shot()
        elif client_input == "BOARD":
            return self.communication_utils.client_send_final_ships_positions()
        else:
            return self.communication_utils.client_send_unknown_command()

    def read_server_response(self, server_response_json, client_socket):
        server_response = self.data_utils.deserialize_json(server_response_json)
        print(server_response)
        if server_response['type'] == "SHOT_REQUEST":
            client_response = self.communication_utils.client_response_for_server_shot(server_response)
            client_response_json = self.data_utils.serialize_to_json(client_response)
            client_socket.sendall(client_response_json)
            server_response_json = client_socket.recv(self.buffer)
            server_response = self.data_utils.deserialize_json(server_response_json)
            print(server_response)
        if server_response['type'] == "GAME_INVITATION" and server_response['status'] == 'OK':
            self.player.coordinates_for_ship_add_to_board()

    def invite_server(self):
        self.communication_utils.protocol_template(message_type = self.communication_utils.message_type[0])

    def start(self):
        with socket.socket(self.internet_address_family, self.socket_type) as client_socket:
            client_socket.connect((self.host, self.port))
            while self.is_running:
                client_input = input("Request: ").upper()
                client_request = self.create_request_to_server(client_input)
                client_request_json = self.data_utils.serialize_to_json(client_request)
                client_socket.sendall(client_request_json)
                server_response_json = client_socket.recv(self.buffer)
                self.read_server_response(server_response_json, client_socket)

                # put there condition on which client_socket will be stopped
                # self.stop()

    def stop(self, client_socket):
        self.is_running = False
        client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.start()
