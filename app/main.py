from typing import List
from jose import jwt, JWTError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from . import database, models, schemas, auth
from sqlalchemy.orm import Session
# from sqlalchemy import


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    wrong_credentials = HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise wrong_credentials
    except JWTError:
        raise wrong_credentials
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise wrong_credentials
    return user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = auth.get_password_hash(user.password)

    new_user = models.User(username = user.username, hashed_password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = auth.create_access_token(data={"sub": user.username})

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/tasks/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    new_task = models.Task(**task.dict(), owner_id = current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.patch("/tasks/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id,models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_task = task_update.dict(exclude_unset=True)
    for key, value in update_task.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)
    return db_task

@app.get("/tasks", response_model=List[schemas.Task])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: models.User = Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).offset(skip).limit(limit).all()
    return tasks


