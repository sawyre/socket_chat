from typing import Set, List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User


class Chat:
    users: Set["User"] = set()
    messages: List[Tuple["User", str]] = []

    def add_user(self, user: "User") -> None:
        self.users.add(user)

    def add_message(self, message, user: "User") -> None:
        self.messages.append((user, message))

    def delete_user(self, user: "User"):
        self.users.remove(user)
