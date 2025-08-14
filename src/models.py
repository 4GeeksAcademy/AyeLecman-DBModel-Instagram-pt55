from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")

    following: Mapped[List["Follower"]] = relationship(back_populates="follower", foreign_keys="[Follower.follower_id]")
    followers: Mapped[List["Follower"]] = relationship(back_populates="followed", foreign_keys="[Follower.followed_id]")
  
class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
      
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    text_comment: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    user: Mapped["User"] = relationship(back_populates="comments")

    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False, index=True)
    user: Mapped["Post"] = relationship(back_populates="comments")

class Follower(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Usuario que sigue
    follower_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    follower: Mapped["User"] = relationship(back_populates="following")

    # Usuario seguido
    followed_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False, index=True)
    followed: Mapped["User"] = relationship(back_populates="followers")
    
    
