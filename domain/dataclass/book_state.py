

from typing import TypedDict


class BookState(TypedDict, total=False):
    brief: str
    plan: dict
    tasks: list
    results: list
    ebook: str