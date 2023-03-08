from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship  # type: ignore

from src.db.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Media(Base):
    file: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='media')  # type: ignore

    def __repr__(self):
        return self.file
