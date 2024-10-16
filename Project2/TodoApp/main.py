from typing import Annotated

from fastapi import FastAPI

from .database import engine
from .models import Base
from .routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/healthcheck")
def heath_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)