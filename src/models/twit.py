from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .media import MediaTwit
    from .user import User


class Twit(Base):
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='twits')  # type: ignore
    media: Mapped['MediaTwit'] = relationship(  # type: ignore
        back_populates='twit', cascade="all, delete-orphan"
    )

    def repr(self) -> str:
        return 'Twit ID={twit_id} of {user}'.format(
            twit_id=self.id, user=self.user.name
        )
