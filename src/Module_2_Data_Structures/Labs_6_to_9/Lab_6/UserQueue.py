from typing_extensions import Optional
from pathlib import Path

from Stack import Stack
from Queue import Queue
from User import User

class UserQueue:
    def __init__(self):
        self.queue = Queue[User]()
        self.served_users = Stack[User]()

    def register(self, user: User):
        self.queue.enqueue(user)

    def serve_next(self) -> Optional[User]:
        if not self.queue.is_empty():
            user = self.queue.dequeue()
            self.served_users.push(user)
            return user
        else:
            print("No hay usuarios en la cola para atender.")
            return None
        
    def save_to_file(self):
        THIS_PATH = Path(__file__).parent

        with open(THIS_PATH / "pending_users.txt", "wt", encoding="utf-8") as pending_file:
            pending_file.writelines(
                "\n".join([f"{user.get_name()} {user.get_id()}" for user in self.queue])
            )

        with open(THIS_PATH / "served_users.txt", "wt", encoding="utf-8") as served_file:
            served_file.writelines(
                "\n".join([f"{user.get_name()} {user.get_id()}" for user in self.served_users])
            )

    def __repr__(self):
        queue_repr = ", ".join([f"{user.get_name()} {user.get_id()}" for user in self.queue])
        served_repr = ", ".join([f"{user.get_name()} {user.get_id()}" for user in self.served_users])
        return f"UserQueue(pending_users=[{queue_repr}], served_users=[{served_repr}])"