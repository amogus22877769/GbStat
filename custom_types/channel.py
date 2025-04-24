from typing import Optional, TypedDict

class ChannelType(TypedDict):
    username: str
    title: Optional[str]
    description: Optional[str]
    subscribers: int
