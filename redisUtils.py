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

def getPayload(buffer):
    match buffer[0]:
        case '+' | '-' | ':':
            separatorIdx = buffer.find(MSG_SEPARATOR)
            return buffer[1:separatorIdx]

                

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

def serialize(data, respType):
    pass
