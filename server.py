import socket
import translators
import datetime


IP = socket.gethostbyname((socket.gethostname()))  # Getting local IPv-4 address
PORT = 1025 + 8   # (Option 8)
query_text = ""  # User text input...
to_lang = ""  # Translate To Language...
is_working = True  # Parameter to close server connection
to_lang_check = True  # Checking the input format of language

# Configuring type of (socket and connection)
# AF_INET is for IPv-4 address and SOCK_STREAM is for TCP / IP connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associating the socket with an IP address and port number:
server_socket.bind((IP, PORT))

# Allowing server to accept connections (only 1 connection is allowed)
server_socket.listen(1)
conn, address = server_socket.accept()
with open("server_logs.txt", "w", encoding="utf-8") as server_logs:
    conn.send("Welcome, this server provides translation! \n"
              "Available commands: /who, /translate, /codes, /stop\n"
              "/who - About author\n"
              "/translate - Begin translation proccess\n"
              "/codes - Codes for translation\n"
              "/stop - Stopping connection".encode("utf-8"))
    while is_working:
        command = conn.recv(256).decode("utf-8")
        if command.upper() == "/translate".upper():
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Used '/translate' command", file=server_logs)
            conn.send("Text to translate: ".encode("utf-8"))
            query_text = conn.recv(256).decode("utf-8")
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Text to translate: {query_text}", file=server_logs)
            conn.send("Translate to (language code): ".encode("utf-8"))
            while to_lang_check:
                try:
                    to_lang = conn.recv(256).decode("utf-8")
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Language code: {to_lang}", file=server_logs)
                    translated_text = translators.bing(query_text=f'{query_text}',
                                                       to_language=f'{to_lang}')
                    to_lang_check = False
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [SERVER] Correct Language Input!", file=server_logs)
                except:
                     print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [SERVER] Wrong language input!", file=server_logs)
                     conn.sendall(f"Exception occurred: Wrong language code input!\nTry again!".encode("utf-8"))
            to_lang_check = True
            conn.send(f"Translation: {translated_text}".encode("utf-8") +
                      "\n".encode("utf-8") +
                      "Enter command: ".encode("utf-8"))
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [SERVER] Translated text: {translated_text}",
                  file=server_logs)
            continue
        if command.upper() == "/who".upper():
            conn.send("Dmitrii Palienko K-28 | Lab2 | Option 8\nEnter command: ".encode("utf-8"))
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Used '/who' command", file=server_logs)
            continue
        if command.upper() == "/codes".upper():
            conn.send("ru, en, uk, zh, de, fr, it, pt, ja, es...\nEnter command: ".encode("utf-8"))
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Used '/codes' command", file=server_logs)
            continue
        if command.upper() == "/stop".upper():
            is_working = False
            conn.send("Connection is closed! (Type anything to finish the process)".encode("utf-8"))
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Used '/stop' command", file=server_logs)
            server_logs.close()
        else:
            conn.send("Uknown command!\nEnter command: ".encode("utf-8"))
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] User{address} Used uknown command", file=server_logs)
            continue
