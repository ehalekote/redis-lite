import pytest
from redisUtils import *

@pytest.mark.parametrize(
    ('buffer', 'expected'),
    [
        # Simple String test cases
         ("+PING", (None, 0)),
         ("+OK\r\n", (SimpleString('OK'), 5)),
         ("+OK\r\n+Next", (SimpleString('OK'), 5)),

         # Errors test cases
         ("-Error message", (None, 0)),
         ("-Error message\r\n", (Error('Error message'), 16)),
         ("-Error message\r\n+Next", (Error('Error message'), 16)),

         # Integer test cases
         (":10", (None, 0)),
         (":10\r\n", (Integer(10), 5)),
         (":10\r\n+Next", (Integer(10), 5)),

         # Bulk String test cases
         ("$-1\r\n", (None, 5)),
         ("$5\r\nhello", (None, 0)),
         ("$0\r\n\r\n", (BulkString(""), 6)),
         ("$5\r\nhello\r\n", (BulkString("hello"), 11)),
         ("$5\r\nhello\r\n+Next", (BulkString("hello"), 11)),
    ]
)
def test_deserialize(buffer, expected):
    actual = deserialize(buffer)
    assert actual == expected