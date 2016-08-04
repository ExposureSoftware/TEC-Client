import unittest
import client
from tkinter import Tk
from unittest.mock import patch


class TestClient(unittest.TestCase):
    def setUp(self):
        mock_socket = self.create_patch('socket.socket')
        mock_socket.send.return_value = 'TESTING'.__len__()
        mock_socket.close.return_value = 0
        mock_socket.connect.return_value = True
        mock_socket._io_refs = 0
        mock_ui = self.create_patch('client.ClientUI')
        self.test_client = client.Client(Tk())
        self.test_client.socket = mock_socket
        self.test_client.ui = mock_ui

    def create_patch(self, module):
        patcher = unittest.mock.patch(module)
        new_patch = patcher.start()
        self.addCleanup(patcher.stop)
        return new_patch

    def tearDown(self):
        self.test_client.quit()

    def test_send(self):
        self.test_client.send('TESTING')
        self.test_client.socket.send.assert_called_with(b'TESTING\r\n')
        self.test_client.socket.close.assert_close_with(self.test_client.socket)

    def test_send_disconnected(self):
        self.test_client.connect = False
        self.test_client.send('TESTING')
        self.test_client.socket.send.assert_not_called()
        self.test_client.ui.parse_output.assert_called_with("No connection -- please reconnect to send commands.\n")


if __name__ == '__main__':
    unittest.main()
