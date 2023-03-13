from typing import TYPE_CHECKING, Any

from sqlalchemy import ForeignKey
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base
from src.models import MediaTwit

if TYPE_CHECKING:
    from .media import Media
    from .user import User


class Twit(Base):
    tweet_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    tweet_data: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='twits')  # type: ignore
    mediatwit: Mapped[list['MediaTwit']] = relationship(  # type: ignore
        back_populates='twit', cascade="all, delete-orphan", lazy='selectin'
    )
    media: AssociationProxy[list['Media']] = association_proxy(  # type: ignore
        'mediatwit',
        'media',
        creator=lambda media: MediaTwit(media=media)
    )
    like: Mapped[list['Like']] = relationship(  # type: ignore
        back_populates='twit', cascade='all, delete-orphan', lazy='selectin'
    )
    liked_users: AssociationProxy[list['User']] = association_proxy(  # type: ignore
        'like', 'user', creator=lambda user: Like(user=user)
    )

    def repr(self) -> str:
        return 'Twit ID={twit_id} of {user}'.format(
            twit_id=self.id, user=self.user.name
        )

    def to_json(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Like(Base):
    twit_id: Mapped[int] = mapped_column(
        ForeignKey('twit.tweet_id'), nullable=False, primary_key=True, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'), nullable=False, primary_key=True, index=True
    )
    twit: Mapped[Twit] = relationship(back_populates='like')  # type: ignore
    user: Mapped['User'] = relationship(lazy='selectin')  # type: ignore
