# coding-challenge-redis

_This is a simplified redis clone based on the [Write Your Own Redis Server](https://codingchallenges.fyi/challenges/challenge-redis) coding challenge_

## Features
- Supports the same operations as the origianl version of Redis including PING, ECHO, GET, and SET
- Supports Redis like data-structures
- Handles multiple concurrent clients

## Get Started

### Prereqs
- Python 3.10
- Flask

### Installation
1. Clone the repository
2. Install the packages listed in the `requirements.txt` file.
```
pip install -r requirements.txt
```

 ### Tests

#### Serialization / Deserialization tests
``` sh
cd utils
pytest redisUtils_test.py
```



## License
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
