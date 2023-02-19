from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type:ignore

from src.db.base import Base

if TYPE_CHECKING:
    from .user import User


class Twit(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='twits')  # type: ignore

    def repr(self) -> str:
        return 'Twit ID={twit_id} of {user}'.format(
            twit_id=self.id, user=self.user.name
        )
