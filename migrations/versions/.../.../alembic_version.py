from alembic import op
import sqlalchemy as sa

# Import the User model from your application's models
from models.user import User

# Import the ApiUsage model from your application's models
from models.api_usage import ApiUsage

# Revision Identifier
revision = 'YOUR_REVISION_ID'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add the users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('username', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('email', sa.String(), unique=True, index=True, nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('api_key', sa.String(), unique=True, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )

    # Add the api_usage table
    op.create_table(
        'api_usage',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('endpoint', sa.String(), nullable=False),
        sa.Column('request_time', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('response_time', sa.Integer(), nullable=False),
        sa.Column('status_code', sa.Integer(), nullable=False),
        sa.Column('request_data', sa.String(), nullable=True),
        sa.Column('response_data', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade():
    # Drop the api_usage table
    op.drop_table('api_usage')

    # Drop the users table
    op.drop_table('users')