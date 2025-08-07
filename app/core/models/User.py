from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String
from .base import Base


class User(Base):
    full_name : Mapped[str] = mapped_column(String(255))
    email : Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password : Mapped[str] = mapped_column(String(512))
    role : Mapped[str] = mapped_column(String(255), default="user")
    accounts = relationship("Account", back_populates="user")
