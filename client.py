import socket
import time
import json
from threading import Thread


HOST = "127.0.0.1"
PORT = 12345
LOGIN = ""
# TODO: Add fine logs


def send_messages(conn: socket.socket) -> None:
    while True:
        inp = input(LOGIN + ": ")
        # TODO: Add alternative IO message flow
        if inp == "\q":
            conn.sendall(bytes(inp, "UTF-8"))
            print("Send closing connection")
            break
        if inp:
            conn.sendall(bytes(inp, "UTF-8"))
        time.sleep(1)

def get_messages(conn: socket.socket) -> None:
    while True:
        data = conn.recv(1024)
        if data:
            if data == b"\q":
                print("Close connection")
                break
            messages = json.loads(data)
            for message in messages:
                print(f"{message[0]}: {message[1]}")


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        print("Enter login: ", end="")
        LOGIN = input()
        if LOGIN:
            s.sendall(bytes(LOGIN, "UTF-8"))

        input_thread = Thread(target=send_messages, args=[s])
        output_thread = Thread(target=get_messages, args=[s])
        input_thread.start()
        output_thread.start()
        input_thread.join()
        output_thread.join()
    print("End program")
