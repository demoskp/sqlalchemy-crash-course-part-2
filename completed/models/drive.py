from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Relationship

from completed.models.base import TimeStampedModel, MetricsModel


class Unit(TimeStampedModel):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    slug = Column(String(40), nullable=False, unique=True)


class Distance(MetricsModel):
    __tablename__ = "distances"


class Economy(MetricsModel):
    __tablename__ = "economies"


class Duration(MetricsModel):
    __tablename__ = "durations"


class Drive(TimeStampedModel):
    __tablename__ = "drives"

    id = Column(Integer, primary_key=True, autoincrement=True)

    distance_id = Column(Integer, ForeignKey("distances.id"), nullable=False, index=True)
    economy_id = Column(Integer, ForeignKey("economies.id"), nullable=False, index=True)
    duration_id = Column(Integer, ForeignKey("durations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    user = Relationship("User", back_populates="drives")
    distance = Relationship("Distance")
    economy = Relationship("Economy")
    duration = Relationship("Duration")
