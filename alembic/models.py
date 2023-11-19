from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, func, ForeignKey

# This is kind of schema of DB
class Post(Base):
    __tablename__="orm_posts"

    id= Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content = Column(String, nullable=False)
    published=Column(Boolean, server_default=text('True'), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

    #created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now'))  # server_default should be in text format 
    


class User(Base):
    __tablename__="users"
    id= Column(Integer, primary_key=True, nullable=False)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "orm_posts.id", ondelete="CASCADE"), primary_key=True)


