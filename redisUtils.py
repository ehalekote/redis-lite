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

def getPayload(buffer, startIdx):
    separatorIdx1 = buffer.find(MSG_SEPARATOR, startIdx)

    match buffer[startIdx]:
        case '+' | '-' | ':':
            return buffer[startIdx+1:separatorIdx1], separatorIdx1-startIdx+2
        case '$':
            if buffer[startIdx+1]=='-' and buffer[startIdx+2]=='1':
                return (None, 5)

            separatorIdx2 = buffer.find(MSG_SEPARATOR, separatorIdx1 + 2)
            payload = buffer[separatorIdx1+2 : separatorIdx2]
            if separatorIdx1 == -1 or separatorIdx2 == -1:
                return None, 0
            return payload, separatorIdx2-startIdx+2

def deserialize(buffer):
    if buffer.find(MSG_SEPARATOR) == -1:
        return (None, 0)
    else:
        payload, length = getPayload(buffer, 0)

        match buffer[0]:
            case '+':
                return (SimpleString(payload), length)
            case '-':
                return (Error(payload), length)
            case ':':
                return (Integer(int(payload)), length)
            case '$':
                return (BulkString(payload), length) if payload != None else (None, length)

def serialize(data, respType):
    pass
