from sqlalchemy import Column, Integer, String
from typing import Optional

from .database import Base


class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    duck1 = Column(String)
    duck2 = Column(String)
 

class Duck(Base):
    __tablename__ = "ducks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    size = Column(String)
    owner = Column(String)