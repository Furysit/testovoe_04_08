"""add admin and test user

Revision ID: 8979d1d0fb63
Revises: 1569ed307890
Create Date: 2025-08-07 22:40:26.807749

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import hashlib

# revision identifiers, used by Alembic.
revision: str = '8979d1d0fb63'
down_revision: Union[str, Sequence[str], None] = '1569ed307890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

user_table = table(
    'user',
    column('id', sa.Integer),
    column('email', sa.String),
    column('full_name', sa.String),
    column('hashed_password', sa.String),
    column('role', sa.String),
)

account_table = table(
    'account',
    column('id', sa.Integer),
    column('user_id', sa.Integer),
    column('balance', sa.Integer),
    column('name', sa.String),
)

def upgrade() -> None:
    op.bulk_insert(user_table, [
        {
            "id": 1,
            "email": "admin@example.com",
            "full_name": "Admin",
            "hashed_password": hashlib.sha256("admin123".encode()).hexdigest(),
            "role": "admin"
        },
        {
            "id": 2,
            "email": "user@example.com",
            "full_name": "User",
            "hashed_password": hashlib.sha256("user123".encode()).hexdigest(),
            "role": "user"
        },
    ])

    op.bulk_insert(account_table, [
        {
            "id": 1,
            "user_id": 2,
            "balance": 1000,
            "name": "Основной счёт"
        }
    ])


def downgrade() -> None:
    op.execute("DELETE FROM account WHERE id = 1")
    op.execute("DELETE FROM user WHERE id IN (1, 2)")