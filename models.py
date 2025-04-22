from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Channel(Base):
    __tablename__ = 'channel'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    username: Mapped[str] = mapped_column(String(32))
    caption: Mapped[str] = mapped_column(String(255))
    subscribers: Mapped[int] = mapped_column(Integer)
