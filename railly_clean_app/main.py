import uvicorn

from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from railly_clean_app import crud, models, schemas
from railly_clean_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World, this is Railly Clean's API."}


@app.post("/robots/", response_model=schemas.Robot)
def create_robot(robot: schemas.Robot, db: Session = Depends(get_db)):
    db_robot = crud.get_robot(db, uuid=robot.uuid)
    if db_robot:
        raise HTTPException(
            status_code=400, detail="Config for uuid already registered."
        )
    return crud.create_robot(db=db, robot=robot)


@app.get("/robots/", response_model=List[schemas.Robot])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_robots(db, skip=skip, limit=limit)
    return users


@app.get("/robots/{uuid}", response_model=schemas.Robot)
def read_user(uuid: str, db: Session = Depends(get_db)):
    db_user = crud.get_robot(db, uuid=uuid)
    if db_user is None:
        raise HTTPException(status_code=404, detail="UUID not found")
    return db_user


@app.put("/robots/", response_model=schemas.Robot)
def update_robot(robot: schemas.Robot, db: Session = Depends(get_db)):
    return crud.update_robot(db, robot=robot)


@app.delete("/robots/{uuid}")
def delete_robot(uuid: str, db: Session = Depends(get_db)):
    crud.delete_robot(db, uuid=uuid)
    return {"message": f"Successfully deleted data for robot with uuid = {uuid}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)