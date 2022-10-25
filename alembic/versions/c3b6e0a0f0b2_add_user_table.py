"""add_user_table

Revision ID: c3b6e0a0f0b2
Revises: 8ad5a4dc94b9
Create Date: 2022-10-25 15:44:40.406876

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3b6e0a0f0b2'
down_revision = '8ad5a4dc94b9'
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
    op.drop_table('users')
    pass
