"""Changed UUID in Payment

Revision ID: 50df3c0b76bc
Revises: 933e713af4e9
Create Date: 2025-08-06 14:29:55.417393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50df3c0b76bc'
down_revision: Union[str, Sequence[str], None] = '933e713af4e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'payment',
        'transaction_id',
        existing_type=sa.VARCHAR(length=36),
        type_=sa.UUID(),
        existing_nullable=False,
        postgresql_using='transaction_id::uuid'
    )

    op.drop_index(op.f('ix_payment_transaction_id'), table_name='payment')
    op.create_unique_constraint(None, 'payment', ['transaction_id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'payment', type_='unique')

    op.alter_column(
        'payment',
        'transaction_id',
        existing_type=sa.UUID(),
        type_=sa.VARCHAR(length=36),
        existing_nullable=False,
        postgresql_using='transaction_id::text'
    )

    op.create_index(op.f('ix_payment_transaction_id'), 'payment', ['transaction_id'], unique=False)
    # ### end Alembic commands ###
