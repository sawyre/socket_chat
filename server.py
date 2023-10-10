import socket
import json
import time
import logging
from threading import Thread
from models.user import User
from models.chat import Chat

# Server settings
HOST = "127.0.0.1"
AVAILABLE_PORT = 12345

# Logger settings
logging.basicConfig(level=logging.INFO, filename="logs.log", filemode="w")

# Global variables
chat = Chat()



def update_chat(message: str, sender: "User"):
    for user in chat.users:
        if user != sender:
            logging.info(
                f"(SEND_MESSAGE) Sender: {sender.name}, Receiver: {user.name}, Message: {message}"
            )
            user.connection.sendall(
                bytes(json.dumps([(sender.name, message)]), "UTF-8")
            )


def get_message(connection: socket.socket, user):
    while True:
        message = connection.recv(1024)
        if not message:
            continue
        message = bytes.decode(message, "UTF-8")
        if message == "\q":
            logging.info(
                f"(CLOSE_CONNECTION) Connection: {connection}, User name: {user.name}"
            )
            connection.sendall(b"\q")
            break
        logging.info(
            f"(GET_MESSAGE) Connection: {connection}, User name: {user.name}, Message: {message}"
        )
        chat.add_message(message, user.name)
        update_chat(message, user)
        time.sleep(1)

def start_chat(connection: socket.socket) -> None:
    global chat
    with connection:
        data = conn.recv(1024)
        if data:
            name = bytes.decode(data, "UTF-8")
            logging.info(
                f"(START_CHAT) Connection: {connection}, User name: {name}"
            )
            user = User(
                connection=connection,
                name=name,
            )
            chat.add_user(user)
            try:
                get_message(connection, user)
            except Exception as e:
                logging.error(
                    f"(EXCEPTION) User name: {name}, Exception: {e}"
                )
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
