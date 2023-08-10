import pytest
from redisUtils import *


@pytest.mark.parametrize(
    ("buffer", "expected"),
    [
        # Simple String test cases
        ("+PING", (None, 0)),
        ("+OK\r\n", (SimpleString("OK"), 5)),
        ("+OK\r\n", (SimpleString("OK"), 5)),
        ("+OK\r\n+Next", (SimpleString("OK"), 5)),
        # Errors test cases
        ("-Error message", (None, 0)),
        ("-Error message\r\n", (Error("Error message"), 16)),
        ("-Error message\r\n+Next", (Error("Error message"), 16)),
        # Integer test cases
        (":10", (None, 0)),
        (":10\r\n", (Integer(10), 5)),
        (":10\r\n+Next", (Integer(10), 5)),
        # Bulk String test cases
        ("$-1\r\n", (BulkString(None), 5)),
        ("$5\r\nhello", (None, 0)),
        ("$0\r\n\r\n", (BulkString(""), 6)),
        ("$5\r\nhello\r\n", (BulkString("hello"), 11)),
        ("$5\r\nhello\r\n+Next", (BulkString("hello"), 11)),
        # Array test cases
        # test case with \r\n in message
        ("*-1\r\n", (Array(None), 5)),
        ("*0\r\n", (Array([]), 4)),
        (
            "*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n",
            (Array([BulkString("hello"), BulkString("world")]), 26),
        ),
        ("*3\r\n:1\r\n:2\r\n:3\r\n", (Array([Integer(1), Integer(2), Integer(3)]), 16)),
        (
            "*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Hello\r\n-World\r\n",
            (
                Array(
                    [
                        Array([Integer(1), Integer(2), Integer(3)]),
                        Array([SimpleString("Hello"), Error("World")]),
                    ]
                ),
                40,
            ),
        ),
    ],
)
def test_deserialize(buffer, expected):
    actual = deserialize(buffer)
    assert actual == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    [
        # Simple String test cases
        ((SimpleString("OK"),), "+OK\r\n"),
        ((SimpleString(""),), "+\r\n"),
        # Errors test cases
        ((Error("Error message"),), "-Error message\r\n"),
        ((Error(""),), "-\r\n"),
        # Integer test cases
        ((Integer(10),), ":10\r\n"),
        # Bulk String test cases
        ((BulkString(""), 0), "$0\r\n\r\n"),
        ((BulkString("hello"), 5), "$5\r\nhello\r\n"),
        ((BulkString(None), 0), "$-1\r\n"),
        # Array test cases
        ((Array(None), 0), "*-1\r\n"),
        ((Array([]), 0), "*0\r\n"),
        ((Array([Integer(1), Integer(2), Integer(3)]), 3), "*3\r\n:1\r\n:2\r\n:3\r\n"),
    ],
)
def test_serialize(data, expected):
    actual = serialize(data)
    assert actual == expected
