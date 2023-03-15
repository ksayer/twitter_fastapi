from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type:ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .twit import Twit


class Follow(Base):
    follower_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False, index=True, primary_key=True
    )
    following_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False, index=True, primary_key=True
    )
    follower: Mapped['User'] = relationship(
        argument=None,
        foreign_keys=[follower_id],
    )
    following: Mapped['User'] = relationship(
        argument=None,
        foreign_keys=[following_id],
    )


class User(Base):
    __table_args__ = (UniqueConstraint('key', name='user_key_unique'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String(64))
    twits: Mapped[List['Twit']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )  # type: ignore
    followers = relationship(
        'User',
        secondary='follow',
        primaryjoin='user.c.id == follow.c.following_id',
        secondaryjoin='user.c.id == follow.c.follower_id',
        lazy='joined',
        join_depth=2,
        back_populates='following',
        overlaps="follower, following",  # type: ignore
    )
    following = relationship(
        'User',
        secondary='follow',
        primaryjoin='user.c.id == follow.c.follower_id',
        secondaryjoin='user.c.id == follow.c.following_id',
        lazy='joined',
        join_depth=2,
        back_populates='followers',
        overlaps="following, follower",  # type: ignore
    )
