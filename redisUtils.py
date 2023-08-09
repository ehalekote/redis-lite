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

def getPayload(buffer):
    separatorIdx1 = buffer.find(MSG_SEPARATOR)

    match buffer[0]:
        case '+' | '-' | ':':
            return buffer[1:separatorIdx1]
        case '$':
            separatorIdx2 = buffer.find(MSG_SEPARATOR, separatorIdx1 + 2)
            payload = buffer[separatorIdx1+2 : separatorIdx2]
            if separatorIdx1 == -1 or separatorIdx2 == -1:
                return None
            return payload

def deserialize(buffer):
    if buffer.find(MSG_SEPARATOR) == -1:
        return None
    else:
        payload = getPayload(buffer)

        match buffer[0]:
            case '+':
                return SimpleString(payload)
            case '-':
                return Error(payload)
            case ':':
                return Integer(int(payload))
            case '$':
                return BulkString(payload) if payload != None else None

def serialize(data, respType):
    pass
