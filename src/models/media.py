from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .twit import Twit
    from .user import User


class Media(Base):
    file: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='media')  # type: ignore
    twits: Mapped['MediaTwit'] = relationship(  # type: ignore
        back_populates='media',
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return self.file


class MediaTwit(Base):
    id = None  # type: ignore
    media_id: Mapped[int] = mapped_column(
        ForeignKey('media.id'), nullable=False, primary_key=True, index=True
    )
    twit_id: Mapped[int] = mapped_column(
        ForeignKey('twit.id'), nullable=False, primary_key=True, index=True
    )
    media: Mapped[Media] = relationship(back_populates='twits')  # type: ignore
    twit: Mapped['Twit'] = relationship(back_populates='media')  # type: ignore
