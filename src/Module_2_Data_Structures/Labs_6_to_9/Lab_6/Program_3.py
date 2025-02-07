from UserQueue import UserQueue
from User import User

def main():
    user_queue = UserQueue()

    user_queue.register(User(name="Fernando-Mendoza", id=45678923))
    user_queue.register(User(name="Ana-Castro", id=78904561))
    user_queue.register(User(name="Carlos-Rodriguez", id=67890234))
    user_queue.register(User(name="Mariana-Lopez", id=56789012))
    user_queue.register(User(name="Andres-Valencia", id=34567891))
    user_queue.save_to_file()

    input("Presiona Enter para continuar...")

    user_queue.serve_next()
    user_queue.serve_next()
    user_queue.save_to_file()

if __name__ == "__main__":
    main()