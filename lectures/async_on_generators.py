import socket
from select import select

tasks = []
to_write = {}
to_read = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 6000))
    server_socket.listen()

    while True:

        yield ('read', server_socket)
        client_socket, addr = server_socket.accept()
        print('Connection from', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:

        yield ('read', client_socket)
        request = client_socket.recv(4096)

        if not request:
            break
        else:
            response = 'Hello, new user\n'.encode()

            yield ('write', client_socket)
            client_socket.send(response)

    client_socket.close()


def event_loop():

    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])

            for socket in ready_to_read:
                tasks.append(to_read.pop(socket))

            for socket in ready_to_write:
                tasks.append(to_write.pop(socket))

        try:
            task = tasks.pop(0)
            reason, socket = next(task)
        except StopIteration:
            print('Done!')
            raise StopIteration

        if reason == 'read':
            to_read[socket] = task
        if reason == 'write':
            to_write[socket] = task


if __name__ == '__main__':
    tasks.append(server())
    event_loop()
