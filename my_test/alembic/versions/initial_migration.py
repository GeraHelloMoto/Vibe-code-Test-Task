"""initial migration

Revision ID: initial
Revises:
Create Date: 2026-03-12
"""
from alembic import op
import sqlalchemy as sa

revision = 'initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('role', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('clientName', sa.String(), nullable=False),
        sa.Column('phone', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('problemText', sa.Text(), nullable=False),
        sa.Column('status', sa.String(), nullable=True, server_default='new'),
        sa.Column('assignedTo', sa.Integer(), nullable=True),
        sa.Column('createdAt', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updatedAt', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['assignedTo'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requests_id'), 'requests', ['id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_requests_id'), table_name='requests')
    op.drop_table('requests')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')