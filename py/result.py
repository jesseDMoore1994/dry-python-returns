from typing import Iterable
from returns.result import Result, Success, Failure, safe

my_users = [
    {"_id": "1", "first": "Jesse", "last": "Moore"},
    {"_id": "2", "first": "John", "last": "Doe"},
    {"_id": "3", "first": "Jane", "last": "Doe"},
]

@safe
def get(users: Iterable[dict], key: str, value: str) -> dict:
    for user in users:
        if user[key] == value:
            return user
    raise RuntimeError(f"Cannot find a user with {key}: {value}!")
