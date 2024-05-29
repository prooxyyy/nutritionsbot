from sqlalchemy import Column, BigInteger, Integer, Enum

from db.base import Base
from enums.enums import Gender, ActivityLevel


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    gender = Column(Enum(Gender), nullable=False)
    age = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    activity_level = Column(Enum(ActivityLevel), nullable=False)
