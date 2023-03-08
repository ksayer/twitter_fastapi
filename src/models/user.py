from typing import TYPE_CHECKING, List

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type:ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .media import Media
    from .twit import Twit


class User(Base):
    __table_args__ = (UniqueConstraint('key', name='user_key_unique'),)

    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String(64))
    twits: Mapped[List['Twit']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )  # type: ignore
    media: Mapped[List['Media']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
    )  # type: ignore

    def repr(self) -> str:
        return 'User ID={user_id}, {name}'.format(user_id=self.id, name=self.name)
