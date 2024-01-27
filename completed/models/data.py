from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, declared_attr

from completed.models import TimeStampedModel


class Unit(TimeStampedModel):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    slug = Column(String(40), nullable=False, unique=True)


class MetricsModel(TimeStampedModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)

    @declared_attr
    def unit(self):
        return relationship("Unit")


class Distance(MetricsModel):
    __tablename__ = "distances"


class Economy(MetricsModel):
    __tablename__ = "economies"


class Duration(MetricsModel):
    __tablename__ = "durations"
