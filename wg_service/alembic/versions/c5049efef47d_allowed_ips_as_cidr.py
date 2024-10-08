"""allowed_ips as CIDR

Revision ID: c5049efef47d
Revises: e27326e27605
Create Date: 2024-08-17 23:33:28.545010

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c5049efef47d"
down_revision: Union[str, None] = "e27326e27605"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        "ALTER TABLE peer ALTER COLUMN allowed_ips SET DATA TYPE cidr USING allowed_ips::cidr;"
    )
    # op.alter_column(
    #     "peer",
    #     "allowed_ips",
    #     existing_type=sa.VARCHAR(),
    #     type_=postgresql.CIDR(),
    #     existing_nullable=False,
    # )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "peer",
        "allowed_ips",
        existing_type=postgresql.CIDR(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
