"""init

Revision ID: 75c040cb2797
Revises: 
Create Date: 2019-06-07 12:32:48.685634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75c040cb2797'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "results",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("search_sequence_name", sa.VARCHAR(255), nullable=False),
        sa.Column("search_sequence", sa.TEXT, nullable=False),
        sa.Column("matched_name", sa.VARCHAR(255)),
        sa.Column("matched_index", sa.Integer),
    )


def downgrade():
    op.drop_table("results")
