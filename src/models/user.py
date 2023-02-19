from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column  # type:ignore

from src.db.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
