import socket
import threading

HEADER = 16
PORT = 9000
IP = socket.gethostbyname(socket.gethostname())
ADDR = (IP, PORT)
FORMAT = 'utf-8'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

sockets_list = [server_socket]
clients = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        msg_len = conn.recv(HEADER)
        message_length = msg_len.decode(FORMAT)
        if not len(msg_len):
            return False
        message_length = int(message_length)
        user = {'header': msg_len, 'data': conn.recv(message_length)}
    except:
        pass
    
    clients[conn] = user
    sockets_list.append(conn)
    ignoreDisconnected = []

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len: 
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            user = clients[conn]
            for client_socket in clients:
                if client_socket != conn:
                    try:
                        client_socket.send(user['header'] + user['data'] + f'{msg_len:<{HEADER}}'.encode(FORMAT) + msg.encode(FORMAT))
                        print(msg)
                    except:
                        ignoreDisconnected.append(client_socket)
            for discon in ignoreDisconnected:
                del clients[discon]
            ignoreDisconnected = []
        else:
            connected = False
    
    conn.close()

def start():
    server_socket.listen(999)
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        conn, addr = server_socket.accept()
        print('Accepted new connection from {}:{}'.format(*addr))
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}')

print("[STARTING] server is starting...")
start()