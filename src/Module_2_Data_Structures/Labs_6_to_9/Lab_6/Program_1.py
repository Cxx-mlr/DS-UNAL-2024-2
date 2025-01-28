from Stack import Stack

def main():
    s = Stack()
    s.push(2)
    s.push(4)
    s.push(6)
    s.push(8)
    s.push(10)

    while not s.is_empty():
        print(s.pop())

if __name__ == "__main__":
    main()