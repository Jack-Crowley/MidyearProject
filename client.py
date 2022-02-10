import socket
import threading
import errno

class Client():
    def __init__(self, username, password):
        print("initialized")
        self.HEADER = 16
        print(1)
        self.PORT = 9000
        print(2)
        self.IP = "3.222.3.116"
        print(3)
        self.ADDR = (self.IP, self.PORT)
        print(4)
        self.FORMAT = 'utf-8'
        print(5)
        self.msg = ""
        print(6)

        self.my_username = username
        print(7)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        print(8)

        self.username = self.my_username.encode(self.FORMAT)
        self.username_header = f"{len(self.username):<{self.HEADER}}".encode(self.FORMAT)
        print(9)

    def send_message(self, msg):
        message = msg.encode(self.FORMAT)
        print(10)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        print(11)
        self.client_socket.send(self.username_header)
        print(12)
        self.client_socket.send(self.username)
        self.client_socket.send(send_length)
        self.client_socket.send(message)
        print(13)
        #try:
        username_header = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
        print(14)
        if username_header != "":
            print(15)
            username_length = int(username_header.strip())
            print(15.5)
            username = self.client_socket.recv(username_length).decode(self.FORMAT)
            print(username)
            print(16)
            message_header = self.client_socket.recv(self.HEADER).decode(self.FORMAT)
            print(17)
            message_length = int(message_header.strip())
            print(18)
            message = self.client_socket.recv(message_length).decode(self.FORMAT)
            print(message)
            print(19)
            return f'{username}:{message}'
        else:
            print("NO MSG")
            return 0
        