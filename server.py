import socket
from utils.redisUtils import deserialize, serialize, SimpleString, BulkString


def handleRequest(respArray, length):
    arr = respArray.data
    if arr[0].data == "PING":
        return (SimpleString("PONG"),)
    if arr[0].data == "ECHO" and len(arr) > 1:
        payload = arr[1].data
        return (BulkString(payload), len(payload))

    return "FAIL"


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
            respArray = dataTuple[0]
            length = dataTuple[1]

            res = handleRequest(respArray, length)
            resSerialized = serialize(res)

            conn.sendall(resSerialized.encode())
