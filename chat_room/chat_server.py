import socket
import threading
from characters.moderator import Moderator
from characters.base_character import BaseCharacter
from characters.bast import Bast
from characters.weasel import VinnieTheWeasel
from characters.conspiracy_carl import ConspiracyCarl
from rag.collection_store import CollectionStore
from collections import deque
import traceback



HOST = '127.0.0.1'
PORT = 65432

clients = []
messages = []

collectionStore = CollectionStore("characters")
moderator = Moderator(collectionStore)
bots: list[BaseCharacter]= [Bast(collectionStore)]
relevantMessages = deque(maxlen=3) # the LLMs get confused with more than 5.

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.sendall(message.encode())
            except:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode()
            messages.append((addr, message))
            broadcast(f"{addr}: {message}", conn)
            # Let bots respond to every message
            print("sending message to bots")
            relevantMessages.append(message)
            for bot in bots:
                bot.on_message(list(relevantMessages), broadcast)
        except Exception as e:
            print(f"Error occurred: {e}")
            traceback.print_exc()
            break
    conn.close()
    clients.remove(conn)
    print(f"Disconnected {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
