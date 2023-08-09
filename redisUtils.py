from dataclasses import dataclass

MSG_SEPARATOR = "\r\n"

@dataclass
class SimpleString:
    data: str

def deserialize(buffer):
    separatorIdx = buffer.find(MSG_SEPARATOR)

    if separatorIdx == -1:
        return None
    else:
        payload = buffer[1:separatorIdx]

        match buffer[0]:
            case '+':
                return SimpleString(payload)

def serialize(data, respType):
    pass
