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
        message_length = int(message_length)
        user = {'header': msg_len, 'data': conn.recv(message_length)}
    except:
        print('unable to get username')
    
    sockets_list.append(conn)
    ignoreDisconnected = []
    connected = True
    while connected:
        try:
            msg_len = conn.recv(HEADER).decode(FORMAT)
            if msg_len: 
                msg_len = int(msg_len)
                msg = conn.recv(msg_len).decode(FORMAT)
                if msg: 
                    print(msg)
                for client_socket in clients:
                    if client_socket != conn:
                        try:
                            clients[client_socket].append(f"{user['header']:<{HEADER}}{user['data']}{msg_len:<{HEADER}}{msg}".encode(FORMAT))
                            client_socket.send(clients[client_socket][0])
                            del clients[client_socket][0]
                        except:
                            ignoreDisconnected.append(client_socket)
                for discon in ignoreDisconnected:
                    del clients[discon]
                ignoreDisconnected = []
            else:
                if clients[conn] != []:
                    conn.send(clients[conn][0])
                    del clients[conn][0]
                else:
                    conn.send("".encode(FORMAT))
        except:
            connected = False
    
    conn.close()

def start():
    server_socket.listen(999)
    print(f"[LISTENING] Server is listening on {IP}")
    while True:
        conn, addr = server_socket.accept()
        clients[conn] = []
        print('Accepted new connection from {}:{}'.format(*addr))
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}')

print("[STARTING] server is starting...")
start()