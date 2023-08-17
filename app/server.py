import socket

from redisUtils import deserialize, serialize, SimpleString, BulkString, Error

memory = {}


def handleRequest(respArray, length):
    arr = respArray.data
    cmdBulkString = arr[0]

    if cmdBulkString.data == "PING":
        return (SimpleString("PONG"),)
    elif cmdBulkString.data == "ECHO" and len(arr) > 1:
        payload = arr[1].data
        return (BulkString(payload), len(payload))
    elif cmdBulkString.data == "SET" and len(arr) > 2:
        setKey = arr[1].data
        setValue = arr[2].data
        memory[setKey] = setValue
        return (SimpleString("OK"),)
    elif cmdBulkString.data == "GET" and len(arr) > 1:
        targetKey = arr[1].data
        if targetKey not in memory:
            return (BulkString(None), 5)
        targetValue = memory[targetKey]
        return (BulkString(targetValue), len(targetValue))

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
