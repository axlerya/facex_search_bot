from collections.abc import AsyncGenerator
from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, text, String, Numeric, Text, JSON
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from config import settings

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    uuid: Mapped[UUID] = mapped_column(
        primary_key=True, server_default=text("uuid_generate_v4()")
    )
    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True)

    searches: Mapped[list["Search"]] = relationship(back_populates="user")


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    file_id: Mapped[str] = mapped_column(Text)
    search_id: Mapped[int] = mapped_column(ForeignKey("searches.id"))

    search: Mapped["Search"] = relationship(back_populates="photos")


class Search(Base):
    __tablename__ = "searches"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    uuid: Mapped[UUID] = mapped_column(
        unique=True, server_default=text("uuid_generate_v4()")
    )

    user_uuid: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"))

    user: Mapped[User] = relationship(back_populates="searches")
    photos: Mapped[list[Photo]] = relationship("Photo", back_populates="search")
    photo_urls: Mapped[list["PhotoLinks"]] = relationship("PhotoLinks", back_populates="search")


class PhotoLinks(Base):
    __tablename__ = "photo_links"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    search_id: Mapped[int] = mapped_column(ForeignKey("searches.id"))
    photo_urls: Mapped[list[str]] = mapped_column(JSON)

    search: Mapped["Search"] = relationship(back_populates="photo_urls")

