from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, String

from .base import Base


class Account(Base):
    balance : Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(100), default="Основной счет") 

    user = relationship("User", back_populates="accounts")
    payments = relationship("Payment", back_populates="account", cascade="all, delete-orphan")