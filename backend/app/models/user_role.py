from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(
        Integer,
        primary_key=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    role_id = Column(
        Integer,
        ForeignKey("roles.id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="roles"
    )

    role = relationship(
        "Role",
        back_populates="users"
    )