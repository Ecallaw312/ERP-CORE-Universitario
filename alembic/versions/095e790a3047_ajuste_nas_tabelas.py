"""ajuste nas tabelas

Revision ID: 095e790a3047
Revises: 242c4fcfd780
Create Date: 2026-05-25 17:32:52.317847
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '095e790a3047'
down_revision: Union[str, Sequence[str], None] = '242c4fcfd780'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema (SQLite-friendly)."""
    # Adicionar coluna 'senha' na tabela users
    op.add_column('users', sa.Column('senha', sa.String(), nullable=False))

    # Criar nova tabela temporária para users com NOT NULL em 'nome'
    op.create_table(
        'users_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('senha', sa.String(), nullable=False),
        sa.Column('perfil', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )

    # Copiar dados da tabela antiga para a nova
    op.execute("""
        INSERT INTO users_new (id, nome, email, senha, perfil, ativo, criado_em)
        SELECT id, nome, email, senha, perfil, ativo, criado_em FROM users
    """)

    # Apagar tabela antiga
    op.drop_table('users')

    # Renomear tabela nova para 'users'
    op.rename_table('users_new', 'users')

    # Para 'modules', recriar a tabela com 'nome' NOT NULL
    op.create_table(
        'modules_new',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('porta', sa.Integer(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )

    op.execute("""
        INSERT INTO modules_new (id, nome, url, porta, ativo, criado_em)
        SELECT id, nome, url, porta, ativo, criado_em FROM modules
    """)

    op.drop_table('modules')
    op.rename_table('modules_new', 'modules')


def downgrade() -> None:
    """Downgrade schema (SQLite-friendly)."""
    # Reverter 'users'
    op.create_table(
        'users_old',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('senha_hash', sa.String(), nullable=True),
        sa.Column('perfil', sa.String(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )

    op.execute("""
        INSERT INTO users_old (id, nome, email, perfil, ativo, criado_em)
        SELECT id, nome, email, perfil, ativo, criado_em FROM users
    """)

    op.drop_table('users')
    op.rename_table('users_old', 'users')

    # Reverter 'modules'
    op.create_table(
        'modules_old',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('nome', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('porta', sa.Integer(), nullable=True),
        sa.Column('ativo', sa.Boolean(), nullable=True),
        sa.Column('criado_em', sa.DateTime(), nullable=True),
    )

    op.execute("""
        INSERT INTO modules_old (id, nome, url, porta, ativo, criado_em)
        SELECT id, nome, url, porta, ativo, criado_em FROM modules
    """)

    op.drop_table('modules')
    op.rename_table('modules_old', 'modules')
