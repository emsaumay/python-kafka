import socket
import struct
import threading

HOST = '127.0.0.1'
PORT = 9092

# Kafka protocol constants
API_VERSIONS_KEY = 18  # API key for ApiVersions request

class KafkaServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Kafka server listening on {self.host}:{self.port}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        try:
            while True:
                # Read the length prefix (4 bytes)
                length_bytes = client_socket.recv(4)
                if not length_bytes:
                    break
                (length,) = struct.unpack('>I', length_bytes)
                data = client_socket.recv(length)
                if not data:
                    break
                # Parse Correlation ID (bytes 4-8)
                correlation_id = struct.unpack('>I', data[4:8])[0]
                # Parse API Key (bytes 0-2)
                api_key = struct.unpack('>H', data[0:2])[0]
                # Parse API Version (bytes 2-4)
                api_version = struct.unpack('>H', data[2:4])[0]
                print(f"Received request: api_key={api_key}, api_version={api_version}, correlation_id={correlation_id}")
                if api_key == API_VERSIONS_KEY:
                    self.handle_api_versions(client_socket, correlation_id)
                else:
                    self.send_error(client_socket, correlation_id)
        finally:
            client_socket.close()

    def handle_api_versions(self, client_socket, correlation_id):
        # Minimal ApiVersions response: correlation_id + empty version list
        response = struct.pack('>I', correlation_id) + b'\x00\x00'  # error_code=0, no versions
        length = struct.pack('>I', len(response))
        client_socket.sendall(length + response)
        print(f"Sent ApiVersions response for correlation_id={correlation_id}")

    def send_error(self, client_socket, correlation_id):
        # Send a generic error response
        response = struct.pack('>I', correlation_id) + b'\x00\x01'  # error_code=1
        length = struct.pack('>I', len(response))
        client_socket.sendall(length + response)
        print(f"Sent error response for correlation_id={correlation_id}")

if __name__ == "__main__":
    server = KafkaServer(HOST, PORT)
    server.start()
