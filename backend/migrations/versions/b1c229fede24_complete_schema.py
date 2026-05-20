"""complete_schema

Revision ID: b1c229fede24
Revises: 189d8cca8f84
Create Date: 2026-05-19 18:28:46.874287
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b1c229fede24"
down_revision: Union[str, Sequence[str], None] = "189d8cca8f84"
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "conversations",

        sa.Column("user_id", sa.Integer(), nullable=False),

        sa.Column("title", sa.String(), nullable=False),

        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),

        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),

        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "email_verifications",

        sa.Column("user_id", sa.Integer(), nullable=False),

        sa.Column("token", sa.String(), nullable=False),

        sa.Column("used", sa.Boolean(), nullable=False),

        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),

        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "password_resets",

        sa.Column("user_id", sa.Integer(), nullable=False),

        sa.Column("token", sa.String(), nullable=False),

        sa.Column("used", sa.Boolean(), nullable=False),

        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),

        sa.PrimaryKeyConstraint("id")
    )

    op.create_table(
        "messages",

        sa.Column(
            "conversation_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "role",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "content",
            sa.String(),
            nullable=False
        ),

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()")
        ),

        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        ),

        sa.ForeignKeyConstraint(
            ["conversation_id"],
            ["conversations.id"]
        ),

        sa.PrimaryKeyConstraint("id")
    )

    op.add_column(
        "sessions",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        )
    )

    op.drop_column(
        "sessions",
        "expires_at"
    )

    op.add_column(
        "sessions",
        sa.Column(
            "expires_at",
            sa.DateTime(),
            nullable=False
        )
    )

    op.drop_constraint(
        "sessions_user_id_fkey",
        "sessions",
        type_="foreignkey"
    )

    op.create_foreign_key(
        None,
        "sessions",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.add_column(
        "users",
        sa.Column(
            "full_name",
            sa.String(),
            nullable=False,
            server_default=""
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default="false"
        )
    )

    op.drop_constraint(
        "users_email_key",
        "users",
        type_="unique"
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True
    )


def downgrade():

    op.drop_index(
        "ix_users_email",
        table_name="users"
    )

    op.drop_column(
        "users",
        "is_deleted"
    )

    op.drop_column(
        "users",
        "full_name"
    )

    op.drop_constraint(
        None,
        "sessions",
        type_="foreignkey"
    )

    op.drop_column(
        "sessions",
        "expires_at"
    )

    op.add_column(
        "sessions",
        sa.Column(
            "expires_at",
            sa.String(),
            nullable=False
        )
    )

    op.drop_column(
        "sessions",
        "is_deleted"
    )

    op.drop_table("messages")
    op.drop_table("password_resets")
    op.drop_table("email_verifications")
    op.drop_table("conversations")