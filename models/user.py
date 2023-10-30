import socket
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import socket


class User:
    name: str
    connection: socket.socket

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __init__(self, connection: socket.socket, name: str) -> None:
        self.name = name
        self.connection = connection
