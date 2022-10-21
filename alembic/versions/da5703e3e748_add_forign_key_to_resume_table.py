"""add forign key to resume table

Revision ID: da5703e3e748
Revises: 74eb32cc835b
Create Date: 2022-10-21 11:18:45.750319

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da5703e3e748'
down_revision = '74eb32cc835b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('resume',sa.Column('owner_id',sa.Integer(),nullable=False)),
    op.create_foreign_key('resume_user_fk',source_table = "resume",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('resume_user_fk',table_name="resume")
    op.drop_column('resume','owner_id')
    pass
