"""Add user activation system

Revision ID: 482df28cc684
Revises: 49cea7292c6c
Create Date: 2026-08-01

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "482df28cc684"
down_revision = "49cea7292c6c"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("users", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "activation_token",
                sa.String(length=100),
                nullable=True
            )
        )


        batch_op.add_column(
            sa.Column(
                "is_active",
                sa.Boolean(),
                nullable=False,
                server_default="false"
            )
        )


    # Generate activation tokens for existing users
    op.execute(
        """
        UPDATE users
        SET activation_token =
        md5(random()::text || clock_timestamp()::text)
        WHERE activation_token IS NULL;
        """
    )


    # Make activation token required
    op.alter_column(
        "users",
        "activation_token",
        nullable=False
    )


def downgrade():

    with op.batch_alter_table("users", schema=None) as batch_op:

        batch_op.drop_column(
            "is_active"
        )


        batch_op.drop_column(
            "activation_token"
        )
