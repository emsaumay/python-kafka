import socket
import struct
import unittest
import threading
import time

HOST = '127.0.0.1'
PORT = 9092

class KafkaServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the server in a background thread
        import kafka_server
        cls.server_thread = threading.Thread(target=kafka_server.server.start, daemon=True)
        cls.server_thread.start()
        time.sleep(1)  # Give server time to start

    def send_request(self, api_key, api_version=0, correlation_id=1234, payload=b''):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        # Build request
        header = struct.pack('>H', api_key) + struct.pack('>H', api_version) + struct.pack('>I', correlation_id)
        request = header + payload
        length = struct.pack('>I', len(request))
        s.sendall(length + request)
        # Read response
        length_bytes = s.recv(4)
        (resp_len,) = struct.unpack('>I', length_bytes)
        resp = s.recv(resp_len)
        s.close()
        return resp

    def test_api_versions(self):
        resp = self.send_request(18)
        self.assertIn(b'\x00\x00', resp)  # error_code=0
        self.assertIn(struct.pack('>H', 18), resp)  # ApiVersions key

    def test_describe_topic_partitions(self):
        resp = self.send_request(50)
        self.assertIn(b'test', resp)  # topic name stub

    def test_fetch(self):
        resp = self.send_request(1)
        self.assertIn(b'hello', resp)  # message stub

    def test_unknown_api(self):
        resp = self.send_request(99)
        self.assertIn(b'\x00\x01', resp)  # error_code=1

if __name__ == "__main__":
    unittest.main()
