from sqlalchemy import Column, Integer, String, Date, UniqueConstraint, Numeric

from database import Base


class RateModel(Base):
    __tablename__ = 'rate'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    cargo_type = Column(String)
    rate = Column(Numeric(10, 2))

    __table_args__ = (
        UniqueConstraint('date', 'cargo_type'),
    )
