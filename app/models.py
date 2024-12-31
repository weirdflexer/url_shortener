from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String
from datetime import datetime


class Model(DeclarativeBase):
    pass


class UrlModel(Model):
    __tablename__ = "URL"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    short_url: Mapped[str] = mapped_column(String(10),
                                           nullable=False,
                                           unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    clicks: Mapped[int] = mapped_column(default=0)
