# import pytest
# from app.redisUtils import Array, BulkString, SimpleString
# from app.server import handleRequest


# @pytest.mark.parametrize(
#     ("respArray", "length", "expected"),
#     [
#         (Array([BulkString("PING")]), 1, SimpleString("PONG")),
#         (
#             Array([BulkString("ECHO"), BulkString("Hello World")]),
#             2,
#             BulkString("Hello World")
#         ),
#     ],
# )
# def test_handleRequest(respArray, length, expected):
#     actual = handleRequest(respArray, length)
#     assert actual == expected

# GET tests

# SET tests
