import socket
import threading

# Server configuration
HOST = "127.0.0.1"  # Localhost
PORT = 55600        # Port for chat server

# Setup socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message: bytes) -> None:
    """Send message to all connected clients."""
    for client in clients:
        client.send(message)


def handle_client(client: socket.socket) -> None:
    """Handle incoming messages from a client."""
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode("utf-8"))
            nicknames.remove(nickname)
            break


def receive_connections() -> None:
    """Accept and manage new client connections."""
    print(f"Server is running on {HOST}:{PORT} ...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive_connections()
