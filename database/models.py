from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import DateTime
from sqlalchemy import func
from datetime import date
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Items(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(
        "date", DateTime, default=func.now(), nullable=True
    )
    supplier: Mapped[str] = mapped_column(String(50), nullable=True)
    is_cat_a: Mapped[bool] = mapped_column(default=False)
    artikelnummer: Mapped[str] = mapped_column(String(50), nullable=True)
    beschreibung: Mapped[str] = mapped_column(String(255), nullable=True)
    farbe: Mapped[str] = mapped_column(String(50), nullable=True)
    ean: Mapped[str] = mapped_column(String(50), nullable=True)
    vpe: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=True)
