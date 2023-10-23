import socket
from data_utils import DataUtils
from communication_utils import CommunicationUtils
from config_variables import HOST, PORT, BUFFER, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.buffer = BUFFER
        self.internet_address_family = INTERNET_ADDRESS_FAMILY
        self.socket_type = SOCKET_TYPE
        self.data_utils = DataUtils()
        self.communication_utils = CommunicationUtils()
        self.is_running = True

    def read_client_request(self, client_request_json):
        return self.data_utils.deserialize_json(client_request_json)

    def create_response_to_client(self, client_request):
        if client_request['type'] == 'GAME_INVITATION':
            return self.communication_utils.game_invitation_response()
        elif client_request['type'] == 'SHOT':
            return self.communication_utils.client_shot_result(client_request)
        elif client_request['type'] == 'SHOT_REQUEST':
            return self.communication_utils.server_shot()
        elif client_request['type'] == 'BOARD':
            return self.communication_utils.ships_positions_server_confirmation()
        elif client_request['type'] == 'RESULT':
            return self.communication_utils.server_shot_response()
        else:
            return self.communication_utils.unknown_command()

    def start(self):
        with socket.socket(self.internet_address_family, self.socket_type) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            client_socket, address = server_socket.accept()
            while self.is_running:
                client_request_json = client_socket.recv(self.buffer)
                client_request = self.read_client_request(client_request_json)
                print(client_request)
                response_to_client = self.create_response_to_client(client_request)
                response_to_client_json = self.data_utils.serialize_to_json(response_to_client)
                client_socket.sendall(response_to_client_json)

                # put there condition on which server_socket will be stopped
                # self.stop()

    def stop(self, server_socket):
        self.is_running = False
        server_socket.close()


if __name__ == "__main__":
    server = Server()
    server.start()
