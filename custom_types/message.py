from typing import TypedDict


class Message(TypedDict):
    id: int
    caption: str
    views: int
    datetime: str


if __name__ == '__main__':
    a: Message['id'] = 'asdasdasd'