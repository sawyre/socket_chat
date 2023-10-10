import socket
import json
from threading import Thread
from typing import TextIO


# Host address
HOST = "127.0.0.1"
PORT = 12345

# Client settings
CHAT_FILE = "chat.txt"

# Global variables
login = ""


def send_messages(conn: socket.socket, chat_file: TextIO) -> None:
    while True:
        inp = input(f"{login} : ")
        if inp == "\q":
            conn.sendall(bytes(inp, "UTF-8"))
            print("Send closing connection")
            chat_file.write(f"Send closing connection\n")
            chat_file.flush()
            break
        if inp:
            conn.sendall(bytes(inp, "UTF-8"))
            chat_file.write(f"{login}: {inp}\n")
            chat_file.flush()

def get_messages(conn: socket.socket, chat_file: TextIO) -> None:
    while True:
        data = conn.recv(1024)

        if data:
            # Check for disconnect message
            if data == b"\q":
                chat_file.write(f"Close connection\n")
                chat_file.flush()
                break

            # TODO: Add error checking
            # TODO: Add showing messages in terminal
            author, message = json.loads(data)
            chat_file.write(f"{author}: {message}\n")
            chat_file.flush()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print("Enter login: ", end="")
        login = input()
        if login:
            s.sendall(bytes(login, "UTF-8"))
        file = open(login + CHAT_FILE, "w+")
        file.write("You entered in chat.\n")
        file.flush()

        input_thread = Thread(target=send_messages, args=[s, file])
        input_thread.start()

        get_messages(s, file)
        input_thread.join()

        file.close()
    print("End program")
