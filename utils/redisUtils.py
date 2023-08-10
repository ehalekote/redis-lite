from dataclasses import dataclass

MSG_SEPARATOR = "\r\n"


@dataclass
class SimpleString:
    data: str


@dataclass
class Error:
    data: str


@dataclass
class Integer:
    data: int


@dataclass
class BulkString:
    data: str


@dataclass
class Array:
    data: list


def getPayload(buffer, startIdx):
    separatorIdx1 = buffer.find(MSG_SEPARATOR, startIdx)

    match buffer[startIdx]:
        case "+" | "-" | ":":
            return buffer[startIdx + 1 : separatorIdx1], separatorIdx1 + 2 - startIdx
        case "$":
            if buffer[startIdx + 1] == "-" and buffer[startIdx + 2] == "1":
                return (None, 5)

            separatorIdx2 = buffer.find(MSG_SEPARATOR, separatorIdx1 + 2)
            payload = buffer[separatorIdx1 + 2 : separatorIdx2]
            if separatorIdx1 == -1 or separatorIdx2 == -1:
                return None, 0
            return payload, separatorIdx2 - startIdx + 2
        case "*":
            if buffer[startIdx + 1] == "-" and buffer[startIdx + 2] == "1":
                return (None, 5)

            arraySize = buffer[startIdx + 1 : separatorIdx1]

            payload = []
            nextIdx = startIdx + 4
            for _ in range(int(arraySize)):
                childPayload, length = deserialize(buffer, nextIdx)
                payload.append(childPayload)
                nextIdx = nextIdx + length

            return (payload, nextIdx - startIdx)


def deserialize(buffer, startIdx=0):
    if buffer.find(MSG_SEPARATOR) == -1:
        return (None, 0)
    else:
        payload, length = getPayload(buffer, startIdx)

        match buffer[startIdx]:
            case "+":
                return (SimpleString(payload), length)
            case "-":
                return (Error(payload), length)
            case ":":
                return (Integer(int(payload)), length)
            case "$":
                return (
                    (None, length)
                    if payload == None and not length
                    else (BulkString(payload), length)
                )
            case "*":
                return (
                    (None, length)
                    if payload == None and not length
                    else (Array(payload), length)
                )


def serialize(dataTuple):
    match dataTuple[0]:
        case SimpleString():
            return f"+{dataTuple[0].data}{MSG_SEPARATOR}"
        case Error():
            return f"-{dataTuple[0].data}{MSG_SEPARATOR}"
        case Integer():
            return f":{dataTuple[0].data}{MSG_SEPARATOR}"
        case BulkString():
            if dataTuple[0].data == None:
                return "$-1\r\n"
            else:
                return (
                    f"${dataTuple[1]}{MSG_SEPARATOR}{dataTuple[0].data}{MSG_SEPARATOR}"
                )
        case Array():
            if dataTuple[0].data == None:
                return "*-1\r\n"
            else:
                serializedData = f"*{dataTuple[1]}{MSG_SEPARATOR}"
                for redisObject in dataTuple[0].data:
                    nextData = None
                    if isinstance(redisObject, BulkString) or isinstance(
                        redisObject, Array
                    ):
                        nextData = (
                            (redisObject, 0)
                            if redisObject.data == None
                            else (redisObject, len(redisObject.data))
                        )
                    else:
                        nextData = (redisObject,)
                    serializedData += serialize(nextData)
                return serializedData
