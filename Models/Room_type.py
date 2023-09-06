from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RoomType(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    # Add other fields as needed

    def __repr__(self):
        return f"<RoomType(id={self.id}, name={self.name})>"
