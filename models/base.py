from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, declared_attr

from main import session

Model = declarative_base()
Model.query = session.query_property()


class TimeStampedModel(Model):
    __abstract__ = True

    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())


class MetricsModel(TimeStampedModel):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Float)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)

    @declared_attr
    def unit(self):
        return relationship("Unit")
