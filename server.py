import socket
from utils.redisUtils import deserialize, handleRequest

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            dataBytes = conn.recv(1024)
            if not dataBytes:
                break
            dataTuple = deserialize(dataBytes.decode("utf-8"))
            data = dataTuple[0]
            length = dataTuple[1]

            res = handleRequest(data, length)

            conn.sendall(res.encode())
