import typing as t
import socket

if t.TYPE_CHECKING:
    import socket

class User:
    name: t.Optional[str]
    connection: socket
    last_message = 0

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __init__(
            self,
            connection: socket.socket,
            name: str,
            last_message: int
    ) -> None:
        self.name = name
        self.connection = connection
        self.last_message = last_message
