from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todos
from .auth import bcrypt_context, get_current_user

router = APIRouter()
router = APIRouter(prefix='/admin', tags=['admin'])


# Dependency injection, calls get_db & get_current_user
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not authenticated.')

    return db.query(Todos).all()


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def read_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Not authenticated.')
    
    todo_model = db.query(Todos)\
        .filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id'))\
        .first() # Will always be one & first because its the PK
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()


