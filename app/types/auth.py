from typing import TypedDict


class CurrentUser(TypedDict):
    sub: str
    email: str
