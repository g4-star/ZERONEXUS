"""add blog and site settings

Revision ID: 5e09b6ad9e73
Revises: 49eaca1d80e7
Create Date: 2026-07-31

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e09b6ad9e73'
down_revision = '49eaca1d80e7'
branch_labels = None
depends_on = None


def upgrade():

    # Create blog_posts table
    op.create_table(
        'blog_posts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('is_published', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # Create site_settings table
    op.create_table(
        'site_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('site_name', sa.String(length=120), nullable=True),
        sa.Column('contact_email', sa.String(length=120), nullable=True),
        sa.Column('whatsapp_number', sa.String(length=50), nullable=True),
        sa.Column('footer_text', sa.String(length=255), nullable=True),
        sa.Column('theme_name', sa.String(length=50), nullable=True),
        sa.Column('mode', sa.String(length=10), nullable=True),
        sa.Column('hero_title', sa.String(length=255), nullable=True),
        sa.Column('hero_subtitle', sa.Text(), nullable=True),
        sa.Column('linkedin_url', sa.String(length=255), nullable=True),
        sa.Column('github_url', sa.String(length=255), nullable=True),
        sa.Column('twitter_url', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():

    op.drop_table('site_settings')
    op.drop_table('blog_posts')
