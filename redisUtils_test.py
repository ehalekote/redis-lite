import pytest
from redisUtils import *

@pytest.mark.parametrize(
    ('buffer', 'expected'),
    [
        # Simple String test cases
         ("+PING", None),
         ("+OK\r\n", SimpleString('OK')),
         ("+OK\r\n+Next", SimpleString('OK')),

         # Errors test cases
         ("-Error message", None),
         ("-Error message\r\n", Error('Error message')),
         ("-Error message\r\n+Next", Error('Error message')),

         # Integer test cases
         (":10", None),
         (":10\r\n", Integer(10)),
         (":10\r\n+Next", Integer(10)),

         # Bulk String test cases
         ("$-1\r\n", None),
         ("$5\r\nhello", None),
         ("$0\r\n\r\n", BulkString("")),
         ("$5\r\nhello\r\n", BulkString("hello")),
         ("$5\r\nhello\r\n+Next", BulkString("hello")),
    ]
)
def test_deserialize(buffer, expected):
    actual = deserialize(buffer)
    assert actual == expected