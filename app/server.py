import socket
import threading

from redisUtils import deserialize, serialize, SimpleString, BulkString, Error


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    memory = {}

    connected = True
    while connected:
        dataBytes = conn.recv(1024)

        if not dataBytes:
            continue

        dataTuple = deserialize(dataBytes.decode("utf-8"))
        respArray = dataTuple[0]
        length = dataTuple[1]

        res = handleRequest(respArray, length, memory)
        resSerialized = serialize(res)

        conn.sendall(resSerialized.encode())

    conn.close()


def handleRequest(respArray, length, memory):
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

print("[STARTING] Server is starting...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
