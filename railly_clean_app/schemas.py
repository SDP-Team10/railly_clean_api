from pydantic import BaseModel


class Robot(BaseModel):
    uuid: str
    table_height: float
    dist_to_wall: float
    pole_width: float
    
    class Config:
        orm_mode = True