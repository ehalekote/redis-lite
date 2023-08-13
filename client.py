import socket
import sys
from utils.redisUtils import serialize, getPayload, Array, BulkString

if len(sys.argv) > 1:
    inputs = sys.argv[1:]
    cmd = Array(list(map(lambda x: BulkString(x), inputs)))
    cmdTuple = (cmd, len(inputs))
    cmdSerialized = serialize(cmdTuple)
else:
    print("ERROR: Please submit a valid Redis command")

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(cmdSerialized.encode())
    data = s.recv(1024).decode()
    payload = getPayload(data, 0)
    res = payload[0]

print(f"{res}")
