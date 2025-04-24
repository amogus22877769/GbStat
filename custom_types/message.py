from typing import TypedDict


class MessageType(TypedDict):
    id: int
    caption: str
    views: int
    datetime: str
    photo_urls: list[str]
    video_urls: list[str]
    sticker_url: str


if __name__ == '__main__':
    a: MessageType['id'] = 'asdasdasd'