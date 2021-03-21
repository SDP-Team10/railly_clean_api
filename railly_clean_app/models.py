from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Robot(Base):
    __tablename__ = "robots"
    
    id = Column(Integer, index=True, )
    uuid = Column(String, primary_key=True,)
    table_height = Column(Float,)
    dist_to_wall = Column(Float,)
    pole_width = Column(Float,)