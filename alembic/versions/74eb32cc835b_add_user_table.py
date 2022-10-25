"""add user table

Revision ID: 74eb32cc835b
Revises: 030dcdbf97f0
Create Date: 2022-10-21 10:47:43.800328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74eb32cc835b'
down_revision = '030dcdbf97f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column("id",sa.Integer(),nullable=False),
    sa.Column("email",sa.String(),nullable=False),
    sa.Column("password",sa.String(),nullable=False),
    sa.Column("created_at",sa.TIMESTAMP(timezone=True),
    server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_constraint('id')
    op.drop_table('users')
    pass
