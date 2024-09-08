from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, ForeignKey

from app.db.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)   
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    def __str__(self):
        return (f"user_id = {self.id} username={self.username}, email={self.email}, ")


class FiveGenerator(Base):
    __tablename__ = 'five_generator'
    short_key = Column(String, nullable=False, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    long_url =  Column(String, nullable=False) 
    domain = Column(String, nullable=False) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class SixGenerator(Base):
    __tablename__ = 'six_generator'
    short_key = Column(String, nullable=False, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    long_url =  Column(String, nullable=False) 
    domain = Column(String, nullable=False) 
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)


class ShortLinkDetails(Base):
    __tablename__ = 'short_link_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    short_key = Column(String, nullable=False)
    device = Column(String)
    client_ip = Column(String)
    country = Column(String)
    city = Column(String)
    browsers = Column(String) 
    OS = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

