from colorama import Fore, Style, init
import socket
import threading
import sys

PORT = 60000
HEADER = 2048
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"


def connect():
    """Establishes connection to the server."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(ADDR)
        print(f"Connected to server at {ADDR}")
        return client
    except Exception as e:
        print(f"[ERROR] Unable to connect to server: {e}")
        return None


def send(client, msg):
    """Sends a message to the server."""
    try:
        client.send(msg.encode(FORMAT))
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")


def receive(client):
    """Continuously receives messages from the server."""
    while True:
        try:
            message = client.recv(HEADER).decode(FORMAT)
            if message:
                sys.stdout.write("\r" + f"{Fore.RED}{message}{Style.NORMAL}\nYou: ")
                sys.stdout.flush()
            else:
                break
        except Exception:
            break


def handle_input(client, username):
    """Handles user input and sends it to the server."""
    send(client, username)  # Send username as the first message
    while True:
        msg = input(f"{username}: ")
        if msg== '!!':
            break
        send(client, f"{Fore.MAGENTA}{username}: {msg}{Style.NORMAL}")


def start():
    """Main function to initialize and start the client."""
    init()
    
    connection = connect()
    username = input("input ur username: ")

    # Start thread to receive messages
    threading.Thread(target=receive, args=(connection,), daemon=True).start()

    try:
        handle_input(connection, username)
    except KeyboardInterrupt:
        print(f"\n{username} has been disconnected!")
    finally:
        send(connection, DISCONNECT_MESSAGE)
        connection.close()
        print('Disconnected')


start()
