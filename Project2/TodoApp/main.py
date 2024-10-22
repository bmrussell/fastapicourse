from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine
from .models import Base
from .routers import admin, auth, todos, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="TodoApp/templates")

app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthcheck")
def heath_check():
    return {'status': 'Healthy'}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)