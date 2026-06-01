"""migration inicial limpa

Revision ID: 0001
Revises: 
Create Date: 2026-06-01
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('senha', sa.String(), nullable=False),
        sa.Column('perfil', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    op.create_table('modulo',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('porta', sa.Integer(), nullable=True, unique=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )

    op.create_table('refresh_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('expira_em', sa.DateTime(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('refresh_tokens')
    op.drop_table('modulo')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
