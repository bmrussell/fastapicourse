from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Todos

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        
        yield db        # Returns first then continues to close connection.
    finally:
        db.close()

# Dependency injection, calls get_db
db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):    
    return db.query(Todos).all()

@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() # Will always be one & first because its the PK
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail='Todo not found.')

class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.post("/todos", status_code=status.HTTP_201_CREATED)
async def read_all(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()

@router.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_all(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() # Will always be one & first because its the PK
    if todo_model is  None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    todo_model.title = todo_request.title    
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
        
    db.add(todo_model)
    db.commit()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() # Will always be one & first because its the PK
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    
