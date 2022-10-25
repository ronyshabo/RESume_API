"""create_resume_table

Revision ID: 8ad5a4dc94b9
Revises: 
Create Date: 2022-10-25 15:42:32.742822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ad5a4dc94b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('my_resume',
        sa.Column('id',sa.String(),nullable=False,autoincrement=True),
        sa.Column('title',sa.String(),nullable=False),
        sa.Column('work_place',sa.String(),nullable=False),
        sa.Column('skills',sa.String(),nullable=False),
        sa.Column('time_of_work',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True)),
    server_default=sa.text('now()'),nullable=False)
        
    pass


def downgrade() -> None:
    op.drop_table('my_resume')
    pass
