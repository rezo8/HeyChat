import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 65432


def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            break


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        threading.Thread(target=receive, args=(s,), daemon=True).start()
        print("Connected to chat. Type messages and press Enter.")
        while True:
            msg = sys.stdin.readline()
            if not msg:
                break
            s.sendall(msg.strip().encode())


if __name__ == "__main__":
    main()
