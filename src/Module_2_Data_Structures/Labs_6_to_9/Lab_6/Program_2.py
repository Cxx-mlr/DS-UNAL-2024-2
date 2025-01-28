from Queue import Queue

def main():
    q = Queue()
    q.enqueue(2)
    q.enqueue(4)
    q.enqueue(6)
    q.enqueue(8)
    q.enqueue(10)

    while not q.is_empty():
        print(q.dequeue())

if __name__ == "__main__":
    main()