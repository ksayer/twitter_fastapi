from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base
from src.models import MediaTwit

if TYPE_CHECKING:
    from .user import User


class Twit(Base):
    tweet_id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    tweet_data: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='twits')  # type: ignore
    mediatwit: Mapped[list['MediaTwit']] = relationship(  # type: ignore
        back_populates='twit', cascade="all, delete-orphan"
    )
    media: AssociationProxy[list['Media']] = association_proxy(
        'mediatwit',
        'media',
        creator=lambda media: MediaTwit(media=media),
    )

    def repr(self) -> str:
        return 'Twit ID={twit_id} of {user}'.format(
            twit_id=self.id, user=self.user.name
        )
