import socket

# Getting local IPv-4 adress
# In case, of not using LAN, we have to specify IP-adress of the server provider
IP = socket.gethostbyname((socket.gethostname()))
PORT = 1025 + 8   # (Option 8)
is_connected = True
# Configuring type of (socket and connection)
# AF_INET is for IPv-4 adress and SOCK_STREAM is for TCP / IP connection
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Making connection to server socket
print("Connecting...")
while is_connected:
    try:
        client_socket.connect((IP, PORT))
        print("Connected to server!")
        is_connected = False
    except:
        continue

with open("client_logs.txt", "w", encoding="utf-8") as client_logs:
    while True:
        try:
            info = client_socket.recv(256).decode("utf-8")
            print(info, file=client_logs)
            print(info)
            text_input = input()
            client_socket.sendall(text_input.encode("utf-8"))
            print(text_input, file=client_logs)
        except:
            break
client_logs.close()