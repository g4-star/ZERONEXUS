"""add profile token to members

Revision ID: 49eaca1d80e7
Revises: 9952291abfd0
Create Date: 2026-07-31

"""

from alembic import op
import sqlalchemy as sa
import secrets


# revision identifiers, used by Alembic.
revision = '49eaca1d80e7'
down_revision = '9952291abfd0'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: add the column as nullable
    with op.batch_alter_table('member_profiles', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('profile_token', sa.String(length=64), nullable=True)
        )

    # Step 2: populate existing rows
    connection = op.get_bind()

    result = connection.execute(
        sa.text('SELECT id FROM member_profiles')
    )

    rows = result.fetchall()

    for row in rows:
        connection.execute(
            sa.text(
                'UPDATE member_profiles '
                'SET profile_token = :token '
                'WHERE id = :id'
            ),
            {
                'token': secrets.token_hex(32),
                'id': row.id
            }
        )

    # Step 3: make the column NOT NULL and unique
    with op.batch_alter_table('member_profiles', schema=None) as batch_op:
        batch_op.alter_column(
            'profile_token',
            existing_type=sa.String(length=64),
            nullable=False
        )

        batch_op.create_unique_constraint(
            'uq_member_profiles_profile_token',
            ['profile_token']
        )


def downgrade():
    with op.batch_alter_table('member_profiles', schema=None) as batch_op:
        batch_op.drop_constraint(
            'uq_member_profiles_profile_token',
            type_='unique'
        )

        batch_op.drop_column('profile_token')
