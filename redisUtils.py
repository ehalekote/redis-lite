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
        case '+' | '-' | ':':
            return buffer[startIdx+1:separatorIdx1], separatorIdx1-startIdx+2
        case '$':
            if buffer[startIdx+1] == '-' and buffer[startIdx+2] == '1':
                return (None, 5)

            separatorIdx2 = buffer.find(MSG_SEPARATOR, separatorIdx1 + 2)
            payload = buffer[separatorIdx1+2: separatorIdx2]
            if separatorIdx1 == -1 or separatorIdx2 == -1:
                return None, 0
            return payload, separatorIdx2-startIdx+2
        case '*':
            if buffer[startIdx+1] == '-' and buffer[startIdx+2] == '1':
                return (None, 5)

            arraySize = buffer[startIdx+1:separatorIdx1]

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
            case '+':
                return (SimpleString(payload), length)
            case '-':
                return (Error(payload), length)
            case ':':
                return (Integer(int(payload)), length)
            case '$':
                return (None, length) if payload == None and not length else (BulkString(payload), length)
            case '*':
                return (None, length) if payload == None and not length else (Array(payload), length)


def serialize(redisObject):
    match redisObject:
        case SimpleString():
            return f'+{redisObject.data}{MSG_SEPARATOR}'
        case Error():
            return f'-{redisObject.data}{MSG_SEPARATOR}'
        case Integer():
            return f':{redisObject.data}{MSG_SEPARATOR}'


deserialize("$-1\r\n")
