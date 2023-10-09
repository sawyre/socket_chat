import socket
import time
import json
from threading import Thread


CHAT_FILE = "chat.txt"
HOST = "127.0.0.1"
PORT = 12345
LOGIN = ""
# TODO: Add fine logs


def send_messages(conn: socket.socket, file) -> None:
    while True:
        inp = input(LOGIN + ": ")
        if inp == "\q":
            conn.sendall(bytes(inp, "UTF-8"))
            print("Send closing connection")
            file.write(f"Send closing connection\n")
            file.flush()
            break
        if inp:
            conn.sendall(bytes(inp, "UTF-8"))
            file.write(f"{LOGIN}: {inp}\n")
            file.flush()
        time.sleep(1)

def get_messages(conn: socket.socket, file) -> None:
    while True:
        data = conn.recv(1024)
        if data:
            if data == b"\q":
                file.write(f"Close connection\n")
                file.flush()
                break
            messages = json.loads(data)
            for message in messages:
                file.write(f"{message[0]}: {message[1]}\n")
                file.flush()



if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print("Enter login: ", end="")
        LOGIN = input()
        if LOGIN:
            s.sendall(bytes(LOGIN, "UTF-8"))
        file = open(LOGIN + CHAT_FILE, "w+")
        file.write("You entered in chat.\n")
        file.flush()

        input_thread = Thread(target=send_messages, args=[s, file])
        output_thread = Thread(target=get_messages, args=[s, file])
        input_thread.start()
        output_thread.start()
        input_thread.join()
        output_thread.join()
        file.close()
    print("End program")
