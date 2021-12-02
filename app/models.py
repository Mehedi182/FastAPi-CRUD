from sqlalchemy import  *
from .database import Base
from datetime import datetime


class User(Base):
    __tablename__= 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    title = Column(String)
    body = Column(String)