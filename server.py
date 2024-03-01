import socket
import json
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


class SendMessageScheme:
    """
    Structure for send message
    """

    @staticmethod
    def create_message(user: User, message: str) -> str:
        dict_message = {"data": {"author": user.name, "message": message}}
        return json.dumps(dict_message)


def update_chat(message: str, sender: "User") -> None:
    """
    Send new message in all users chats
    """
    deleted_users = set()
    for user in chat.users:
        if user != sender:
            logging.info(
                f"(SEND_MESSAGE) Sender: {sender.name}, Receiver: {user.name}, Message: {message}"
            )
            try:
                user.connection.sendall(
                    bytes(SendMessageScheme.create_message(sender, message), "UTF-8")
                )
            except Exception as e:
                # for users who unexpectedly disconnected
                logging.exception(f"(EXCEPTION) User name: {user.name}, Exception: {e}")
                deleted_users.add(user)
    chat.users.difference_update(deleted_users)


def get_message(connection: socket.socket, user) -> None:
    """
    Wait user messages, add it in list and update all other user chats
    """
    while True:
        raw_message = connection.recv(1024)
        if not raw_message:
            continue
        message = bytes.decode(raw_message, "UTF-8")
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


def run_chat(connection: socket.socket) -> None:
    """
    Create chat user, run function of waiting his messages and delete user after disconnection
    """
    global chat
    with connection:
        data = conn.recv(1024)
        if data:
            name = bytes.decode(data, "UTF-8")
            logging.info(f"(START_CHAT) Connection: {connection}, User name: {name}")
            user = User(connection=connection, name=name)
            chat.add_user(user)
            try:
                get_message(connection, user)
            except Exception as e:
                logging.exception(f"(EXCEPTION) User name: {name}, Exception: {e}")
            finally:
                chat.delete_user(user)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, AVAILABLE_PORT))
        s.listen()
        while True:
            conn, _ = s.accept()
            thread = Thread(target=run_chat, args=(conn,))
            thread.start()
