from DB.conection import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = 'tbUsers'
    id = Column(Integer, primary_key=True,autoincrement="auto")
    name = Column(String(85))
    age = Column(Integer)
    email = Column(String(85))