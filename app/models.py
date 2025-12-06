from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import UniqueConstraint, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .extensions import db

# ============================
# Base mixins
# ============================

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=db.func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now()
    )


# ============================
# Owner
# ============================

class Owner(db.Model, TimestampMixin):
    __tablename__ = "owners"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    address: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]

    horses: Mapped[List["Horse"]] = relationship(
        "Horse", back_populates="owner", cascade="all, delete-orphan"
    )


# ============================
# Horse
# ============================

class Horse(db.Model, TimestampMixin):
    __tablename__ = "horses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False, index=True)
    sex: Mapped[str] = mapped_column(
        db.Enum("male", "female", name="sex_enum"), nullable=False
    )
    birth_date: Mapped[Optional[date]]

    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("owners.id", ondelete="SET NULL")
    )
    owner: Mapped[Optional[Owner]] = relationship(
        "Owner", back_populates="horses"
    )

    entries: Mapped[List["Entry"]] = relationship(
        "Entry", back_populates="horse", cascade="all, delete-orphan"
    )


# ============================
# Jockey
# ============================

class Jockey(db.Model, TimestampMixin):
    __tablename__ = "jockeys"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False, index=True)
    address: Mapped[Optional[str]]
    birth_date: Mapped[Optional[date]]
    rating: Mapped[float] = mapped_column(db.Float, default=0.0)

    entries: Mapped[List["Entry"]] = relationship(
        "Entry", back_populates="jockey", cascade="all, delete-orphan"
    )


# ============================
# Event
# ============================

class Event(db.Model, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)

    # ✔ тесты и схемы требуют field name
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)

    title: Mapped[Optional[str]] = mapped_column(db.String(200))
    venue: Mapped[str] = mapped_column(db.String(200), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), nullable=False, index=True
    )

    entries: Mapped[List["Entry"]] = relationship(
        "Entry", back_populates="event", cascade="all, delete-orphan"
    )



# ============================
# Entry — many-to-many with extra fields
# ============================

class Entry(db.Model, TimestampMixin):
    __tablename__ = "entries"

    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    horse_id: Mapped[int] = mapped_column(
        ForeignKey("horses.id", ondelete="CASCADE"), primary_key=True
    )
    jockey_id: Mapped[int] = mapped_column(
        ForeignKey("jockeys.id", ondelete="CASCADE"), primary_key=True
    )

    place: Mapped[Optional[int]] = mapped_column(db.Integer)
    time_ms: Mapped[Optional[int]] = mapped_column(db.Integer)

    event = relationship("Event", back_populates="entries")
    horse = relationship("Horse", back_populates="entries")
    jockey = relationship("Jockey", back_populates="entries")

    __table_args__ = (
        UniqueConstraint("event_id", "horse_id", name="uq_entry_event_horse"),
        UniqueConstraint("event_id", "jockey_id", name="uq_entry_event_jockey"),
        UniqueConstraint(
            "event_id", "horse_id", "jockey_id", name="uq_entry_event_pair"
        ),
        CheckConstraint("place IS NULL OR place > 0", name="ck_place_positive"),
        CheckConstraint("time_ms IS NULL OR time_ms >= 0", name="ck_time_ms_nonnegative"),
    )


# ============================
# Auth models
# ============================

from werkzeug.security import generate_password_hash, check_password_hash

user_roles = db.Table(
    "user_roles",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(db.Model, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        db.String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    full_name: Mapped[Optional[str]]

    owner_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("owners.id", ondelete="SET NULL")
    )
    jockey_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("jockeys.id", ondelete="SET NULL")
    )

    roles = relationship("Role", secondary=user_roles, back_populates="users")

    # password helpers
    def set_password(self, raw: str):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)


class Role(db.Model, TimestampMixin):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        db.String(50), unique=True, nullable=False
    )

    users = relationship("User", secondary=user_roles, back_populates="roles")
