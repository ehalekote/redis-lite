import pytest
from redisUtils import *

@pytest.mark.parametrize(
    ('buffer', 'expected'),
    [
        # Simple String test cases
         ("+PING", None),
         ("+OK\r\n", SimpleString('OK')),
         ("+OK\r\n+Next", SimpleString('OK'))
    ]
)
def test_deserialize(buffer, expected):
    actual = deserialize(buffer)
    assert actual == expected