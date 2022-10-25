"""resume table

Revision ID: 8d48578e6ad1
Revises: 129d32b27a2d
Create Date: 2022-10-25 16:49:03.198757

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d48578e6ad1'
down_revision = '129d32b27a2d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('resume',
        sa.Column('id',sa.String(),nullable=False,autoincrement=True),
        sa.Column('title',sa.String(),nullable=False),
        sa.Column('work_place',sa.String(),nullable=False),
        sa.Column('skills',sa.String(),nullable=False),
        sa.Column('time_of_work',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True)),
    server_default=sa.text('now()'),nullable=False)
    pass


def downgrade() -> None:
    op.drop_table('resume')
    pass
