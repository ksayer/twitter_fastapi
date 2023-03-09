from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .twit import Twit


class Media(Base):
    file: Mapped[str]

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
    media: Mapped[Media] = relationship()  # type: ignore
    twit: Mapped['Twit'] = relationship(back_populates='mediatwit')  # type: ignore
