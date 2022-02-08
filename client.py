import socket
import threading
import errno

class Client():
    def __init__(self, username, password):
        self.HEADER = 16
        self.PORT = 9000
        self.IP = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = 'utf-8'
        self.msg = ""

        self.my_username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.client_socket.setblocking(False)

        self.username = self.my_username.encode(self.FORMAT)
        self.username_header = f"{len(self.username):<{self.HEADER}}".encode(self.FORMAT)

    def send_message(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client_socket.send(self.username_header)
        self.client_socket.send(self.username)
        self.client_socket.send(send_length)
        self.client_socket.send(message)
        return f'Printed out {msg}'

    # while True:
    #     message = input(f'{my_username} > ')
    #     send(message)

    #     try:
    #         while True:
    #             username_header = client_socket.recv(HEADER)
    #             if not len(username_header):
    #                 print('Connection closed by the server')
    #                 exit()
    #             username_length = int(username_header.decode(FORMAT).strip())
    #             username = client_socket.recv(username_length).decode(FORMAT)
    #             message_header = client_socket.recv(HEADER)
    #             message_length = int(message_header.decode(FORMAT).strip())
    #             message = client_socket.recv(message_length).decode(FORMAT)

    #             print(f'{username} > {message}')
    #     except IOError as e:
    #         if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
    #             print('Reading error: {}'.format(str(e)))
    #             exit()
    #     except Exception as e:
    #         # Any other exception - something happened, exit
    #         print('Reading error: '.format(str(e)))
    #         exit()

    def recieve(self):
        while True:
            try:
                while True:
                    username_header = self.client_socket.recv(self.HEADER)
                    if not len(username_header):
                        print('Connection closed by the server')
                        exit()
                    username_length = int(username_header.decode(self.FORMAT).strip())
                    username = self.client_socket.recv(username_length).decode(self.FORMAT)
                    message_header = self.client_socket.recv(self.HEADER)
                    message_length = int(message_header.decode(self.FORMAT).strip())
                    message = self.client_socket.recv(message_length).decode(self.FORMAT)
                    print(f'{username} > {message}')
            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    exit()
            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                exit()

jack = Client("Jack", "Bad")
jack.send_message("Jack is bad")