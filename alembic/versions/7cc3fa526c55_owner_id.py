"""owner_id

Revision ID: 7cc3fa526c55
Revises: d0a9d4000fad
Create Date: 2022-10-25 16:49:22.165808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7cc3fa526c55"
down_revision = "d0a9d4000fad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("resume", sa.Column("owner_id", sa.Integer(), nullable=False)),
    op.create_foreign_key(
        "resume_user_fk",
        source_table="resume",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )
    pass


def downgrade() -> None:
    op.drop_constraint("resume_user_fk", table_name="resume")
    op.drop_column("resume", "owner_id")
    pass
