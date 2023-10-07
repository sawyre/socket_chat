import typing as t

if t.TYPE_CHECKING:
    from models.user import User


class Chat:
    users: t.Set["User"] = set()
    messages: t.List[t.Tuple["User", str]] = []

    def add_user(self, user: "User") -> None:
        self.users.add(user)

    def add_message(self, message, user: "User") -> None:
        self.messages.append((user, message))

    def delete_user(self, user: "User"):
        self.users.remove(user)
