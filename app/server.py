import socket
import threading
import time

from redisUtils import deserialize, serialize, SimpleString, BulkString, Error

memory = {}
lock = threading.Lock()


def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

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


def calculateExpiry(type, value):
    if not type and not value:
        return float("inf")

    value = float(value)
    timestamp = time.time()

    match type:
        case "EX":
            timestamp += value
        case "PX":
            timestamp += value / 1000
        case "EXAT":
            timestamp = value
        case "PXAT":
            timestamp = value / 1000

    return timestamp


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
        expiryType = arr[3].data if len(arr) > 3 else None
        expiryValue = arr[4].data if len(arr) > 3 else None
        evictionTime = calculateExpiry(expiryType, expiryValue)
        with lock:
            memory[setKey] = (setValue, evictionTime)
        return (SimpleString("OK"),)
    elif cmdBulkString.data == "GET" and len(arr) > 1:
        targetKey = arr[1].data

        if targetKey not in memory:
            return (BulkString(None), 5)

        targetTuple = memory[targetKey]
        expiry = targetTuple[1]

        if time.time() < expiry:
            targetValue = targetTuple[0]
            return (BulkString(targetValue), len(targetValue))
        else:
            del memory[targetKey]
            return (BulkString(None), 5)

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
