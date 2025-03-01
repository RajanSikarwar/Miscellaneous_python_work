import socket
import select
import errno
import sys

HEADER_LEN = 10

IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((IP,PORT))
client_socket.setblocking(False)

username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LEN}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    
    if message:
        message = message.encode("utf-8")
        message_header = f"{len(message) :< {HEADER_LEN}}".encode("utf-8")
        client_socket.send(message_header + message)

    try:
        while True:
            # receive things
            username_header = client_socket.recv(HEADER_LEN)
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_len = int(username_header.decode("utf-8").strip())
            username =  client_socket.recv(username_len).decode("utf-8")

            message_header = client_socket.recv(HEADER_LEN)
            message_len = int(message_header.decode("utf-8"))
            message = client_socket.recv(message_len).decode("utf-8")

            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('reading error',str(e))
            sys.exit()
        continue


    except Exception as e:
        print("General Error",str(e))
        sys.exit()