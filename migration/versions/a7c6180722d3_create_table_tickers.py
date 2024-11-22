"""create table tickers

Revision ID: a7c6180722d3
Revises: 808481e6bc64
Create Date: 2024-11-21 12:21:43.422941

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7c6180722d3'
down_revision: Union[str, None] = '808481e6bc64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('''
        CREATE TABLE invest."tickers" (
            "id" INTEGER NOT NULL UNIQUE GENERATED BY DEFAULT AS IDENTITY,
            "name" VARCHAR(255) NOT NULL,
            "ticker_type_id" BIGINT NOT NULL,
            PRIMARY KEY("id")
        );
    ''')


def downgrade() -> None:
    op.execute('''
        DROP TABLE invest."tickers";
    ''')
