from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone

class User(UserMixin , db.Model):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(256))
    image: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255), default='default.jpg')
    address: so.Mapped[str] = so.mapped_column(sa.String(255))
    zipcode: so.Mapped[str] = so.mapped_column(sa.String(5))
    phone: so.Mapped[str] = so.mapped_column(sa.String(15), unique=True)
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    is_active: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=True)
    last_login: so.Mapped[Optional[sa.DateTime]] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone('Europe/Helsinki')))
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone('Europe/Helsinki')))
    updated_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone('Europe/Helsinki')), onupdate=lambda: datetime.now(timezone('Europe/Helsinki')))

    def __repr__(self) -> str:
        return f"<User {self.email}>"
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    

class Todo(db.Model):
    __tablename__ = 'todos'
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(255))
    # status with enum values of 'pending', 'completed', 'in-progress'
    status: so.Mapped[str] = so.mapped_column(sa.String(20))
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
    date_todo: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime,nullable=False, default=lambda: datetime.now(timezone('Europe/Helsinki')))    
    created_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone('Europe/Helsinki')))
    updated_at: so.Mapped[sa.DateTime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone('Europe/Helsinki')), onupdate=lambda: datetime.now(timezone('Europe/Helsinki')))
    
    
    
