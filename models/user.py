import typing as t
import socket

if t.TYPE_CHECKING:
    import socket

class User:
    name: t.Optional[str]
    connection: socket.socket
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __init__(self, connection: socket.socket, name: str) -> None:
        self.name = name
        self.connection = connection
