from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError

from . import models, schemas


def get_robot(db: Session, uuid: str):
    return db.query(models.Robot).filter(models.Robot.uuid == uuid).first()


def get_robots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Robot).offset(skip).limit(limit).all()


def create_robot(db: Session, robot: schemas.Robot):
    db_robot = models.Robot(
        uuid=robot.uuid,
        table_height=robot.table_height,
        dist_to_wall=robot.dist_to_wall,
        pole_width=robot.pole_width,
    )
    db.add(db_robot)
    try:
        db.commit()
        db.refresh(db_robot)
        return db_robot
    except InvalidRequestError as err:
        db.rollback()
        raise err

def update_robot(db: Session, robot: schemas.Robot):
    db_robot = get_robot(db, robot.uuid)
    if db_robot is None:
        return None

    # Update model class variable from requested fields
    for var, value in vars(robot).items():
        setattr(db_robot, var, value) if value else None

    db.add(db_robot)
    db.commit()
    db.refresh(db_robot)
    return db_robot


def delete_robot(db: Session, uuid: str):
    db.query(models.Robot).filter(models.Robot.uuid == uuid).delete()
    try:
        db.commit()
        return True
    except InvalidRequestError as err:
        db.rollback()
        raise err