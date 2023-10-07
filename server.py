import socket
import json
import time
from threading import Thread
from models.user import User
from models.chat import Chat


HOST = "127.0.0.1"
AVAILABLE_PORT = 12345
chat = Chat()


class Message:
    message: str
    last_message: int

def update_chat(connection: socket.socket, user: "User"):
    send_messages = []
    for message in chat.messages[(user.last_message + 1):]:
        if message[0] != user.name:
            send_messages.append(message)
    connection.sendall(bytes(json.dumps(send_messages), "UTF-8"))
    user.last_message = len(chat.messages) - 1


def get_message(connection: socket.socket, user):
    while True:
        message = connection.recv(1024)
        if not message:
            continue
        message = bytes.decode(message, "UTF-8")
        if message == "\q":
            print("CLOSE_CONNECTION")
            print(f"Connection: {connection}, User name: {user.name}")
            connection.sendall(b"\q")
            break
        print("GET_MESSAGE")
        print(f"Connection: {connection}, User name: {user.name}, Message: {message}")
        chat.add_message(message, user.name)
        update_chat(connection, user)
        time.sleep(1)

def start_chat(connection: socket.socket) -> None:
    global chat
    with connection:
        name = conn.recv(1024)
        if name:
            print("START_CHAT")
            print(f"Connection: {connection}, User name: {name}")
            user = User(
                connection=connection,
                name=bytes.decode(name, "UTF-8"),
                last_message=len(chat.messages) - 1
            )
            chat.add_user(user)
            try:
                get_message(connection, user)
            except Exception as e:
                print("EXCEPTION")
                print(f"User name: {name}")
            finally:
                chat.delete_user(user)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, AVAILABLE_PORT))
        s.listen()
        while True:
            conn, _ = s.accept()
            thread = Thread(target=start_chat, args=(conn,))
            thread.start()
