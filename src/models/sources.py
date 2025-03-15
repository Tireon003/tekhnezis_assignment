from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class Sources(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str]
    url: Mapped[str]
    xpath: Mapped[str]
