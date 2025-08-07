from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base



class Payment(Base):
    # payment_id: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid.uuid4()), unique=True )
    transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), unique=True)
    amount : Mapped[int] = mapped_column(Integer)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"))

    account = relationship("Account", back_populates="payments")    