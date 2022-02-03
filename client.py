import socket
import errno

HEADER = 16
PORT = 9000
IP = 'ec2-3-94-90-43.compute-1.amazonaws.com'
ADDR = (IP, PORT)
FORMAT = 'utf-8'

my_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.setblocking(False)

username = my_username.encode(FORMAT)
username_header = f"{len(username):<{HEADER}}".encode(FORMAT)
client_socket.send(username_header)
client_socket.send(username)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client_socket.send(send_length)
    client_socket.send(message)

while True:
    message = input(f'{my_username} > ')
    send(message)

    try:
        while True:
            username_header = client_socket.recv(HEADER)
            if not len(username_header):
                print('Connection closed by the server')
                exit()
            username_length = int(username_header.decode(FORMAT).strip())
            username = client_socket.recv(username_length).decode(FORMAT)
            message_header = client_socket.recv(HEADER)
            message_length = int(message_header.decode(FORMAT).strip())
            message = client_socket.recv(message_length).decode(FORMAT)

            print(f'{username} > {message}')
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            exit()
    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        exit()