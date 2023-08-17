import socket

from redisUtils import deserialize, serialize, SimpleString, BulkString, Error


def handleRequest(respArray, length):
    arr = respArray.data
    cmdBulkString = arr[0]
    if cmdBulkString.data == "PING":
        return (SimpleString("PONG"),)
    if cmdBulkString.data == "ECHO" and len(arr) > 1:
        payload = arr[1].data
        return (BulkString(payload), len(payload))

    return (Error("Invalid or unsupported command"),)


HOST = "127.0.0.1"
PORT = 6379

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        print(f"Connected by {addr}")

        dataBytes = conn.recv(1024)

        dataTuple = deserialize(dataBytes.decode("utf-8"))
        respArray = dataTuple[0]
        length = dataTuple[1]

        res = handleRequest(respArray, length)
        resSerialized = serialize(res)

        conn.sendall(resSerialized.encode())
        conn.close()
