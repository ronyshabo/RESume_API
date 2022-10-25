"""add_forign_key

Revision ID: 4a84caae2075
Revises: c3b6e0a0f0b2
Create Date: 2022-10-25 15:45:36.005155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a84caae2075'
down_revision = 'c3b6e0a0f0b2'
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
