import socket
import threading
import tkinter as tk

# Server configuration
HOST = "127.0.0.1"
PORT = 55600

# Ask for nickname in console
nickname = input("Enter your nickname: ")

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# --- GUI Setup ---
root = tk.Tk()
root.title(f"Chat Room - {nickname}")

chat_area = tk.Text(root, height=20, width=50, bg="white", state="disabled")
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=10)


def send_message():
    """Send a message to the server."""
    message = f"{nickname}: {entry.get()}"
    client.send(message.encode("utf-8"))
    entry.delete(0, tk.END)


send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10, pady=10)


def receive_messages():
    """Receive messages from the server and display them."""
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            chat_area.config(state="normal")
            chat_area.insert(tk.END, message + "\n")
            chat_area.config(state="disabled")
            chat_area.see(tk.END)
        except:
            print("Disconnected from server.")
            client.close()
            break


# Thread to listen for messages
thread = threading.Thread(target=receive_messages, daemon=True)
thread.start()

# Start GUI loop
root.mainloop()
