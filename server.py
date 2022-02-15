from posixpath import split
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

with open('nothing.txt') as data: nstring = data.read().strip()

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        msg_len = conn.recv(HEADER)
        message_length = msg_len.decode(FORMAT)
        message_length = int(message_length)
        user = {'header': message_length, 'data': conn.recv(message_length).decode(FORMAT)}
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
                if msg != nstring: 
                    print(msg, "message")
                    if threading.active_count() != 2:
                        for client_socket in clients:
                            if client_socket != conn:
                                try:
                                    clients[client_socket].append(f"{user['header']:<{HEADER}}:{user['data']}:{msg_len:<{HEADER}}:{msg}")
                                    split_msg = clients[client_socket][0].split(":")
                                    print(split_msg)
                                    client_socket.send(split_msg[0].encode(FORMAT))
                                    client_socket.send(split_msg[1].encode(FORMAT))
                                    client_socket.send(split_msg[2].encode(FORMAT))
                                    client_socket.send(''.join(split_msg[3:]).encode(FORMAT))
                                    del clients[client_socket][0]
                                except:
                                    ignoreDisconnected.append(client_socket)
                    else:
                        conn.send(f"{nstring:<{HEADER}}".encode(FORMAT))
                    for discon in ignoreDisconnected:
                        del clients[discon]
                    ignoreDisconnected = []
                else:
                    if len(clients[conn]) != 0:
                        split_msg = clients[client_socket][0].split(":")
                        client_socket.send(split_msg[0].encode(FORMAT))
                        client_socket.send(split_msg[1].encode(FORMAT))
                        client_socket.send(split_msg[2].encode(FORMAT))
                        client_socket.send(''.join(split_msg[3:]).encode(FORMAT))
                        del clients[conn][0]
                    else:
                        conn.send(nstring.encode(FORMAT))
            else:
                connected = False
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