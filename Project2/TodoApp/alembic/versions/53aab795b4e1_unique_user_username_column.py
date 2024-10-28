"""unique user.username column

Revision ID: 53aab795b4e1
Revises: 9f61e5cc11d1
Create Date: 2024-10-22 16:35:22.703213

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '53aab795b4e1'
down_revision: Union[str, None] = '9f61e5cc11d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(constraint_name='unique_username',
                                table_name='users', 
                                columns=['username'])

def downgrade() -> None:
    op.drop_constraint(constraint_name='unique_username', table_name='users')
