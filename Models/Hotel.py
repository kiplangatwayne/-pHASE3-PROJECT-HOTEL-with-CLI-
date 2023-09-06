from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    rating = Column(Float)
    city_id = Column(Integer, ForeignKey("cities.id"))
    # rooms = relationship("Room", back_populates="hotel")

    def __repr__(self):
        return f"<Hotel(id={self.id}, name={self.name})>"
