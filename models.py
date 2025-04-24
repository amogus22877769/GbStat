from typing import List, Optional
from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy.ext.declarative import DeferredReflection

class Base(DeclarativeBase):
    pass

class Reflected(DeferredReflection):
    __abstract__ = True

class Channel(Base):
    __tablename__ = 'channel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    title: Mapped[str] = mapped_column(String(128), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    subscribers: Mapped[int] = mapped_column(Integer, nullable=True)
    origin_messages: Mapped[List['Message']] = relationship()
    changes: Mapped[List['ChannelChange']] = relationship()
    type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_identity": "channel",
        "polymorphic_on": "type",
    }


class Message(Base):
    __tablename__ = 'message'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_in_channel: Mapped[int] = mapped_column(Integer)
    channel_username: Mapped[str] = mapped_column(ForeignKey('channel.username'))
    caption: Mapped[Optional[str]] = mapped_column(String(4096))
    views: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    create_date: Mapped[datetime] = mapped_column(DateTime)
    photo_urls: Mapped[Optional[List['PhotoURL']]] = relationship()
    video_urls: Mapped[Optional[List['VideoURL']]] = relationship()
    sticker_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    changes: Mapped[List['MessageChange']] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "message",
    }

class MessageChange(Message):
    record_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    message_id: Mapped[int] = mapped_column(ForeignKey('message.id'), nullable=True)

    __mapper_args__ = {
    "polymorphic_identity": "message_change",
}

class ChannelChange(Channel):
    record_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    channel_username: Mapped[str] = mapped_column(ForeignKey('channel.username'), nullable=True)
    
    __mapper_args__ = {
    "polymorphic_identity": "channel_change",
}

class URL(Base):
    __tablename__ = 'url'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(ForeignKey('message.id'))
    url: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_on": "type",
        "polymorphic_identity": "url",
    }

class PhotoURL(URL):
    __mapper_args__ = {
        "polymorphic_identity": "photo_url",
    }

class VideoURL(URL):
    __mapper_args__ = {
    "polymorphic_identity": "video_url",
}

