from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite
#SQLALCHEMY_DATABSE_URL = 'sqlite:///./todosapp.db'
#engine = create_engine(SQLALCHEMY_DATABSE_URL, connect_args={'check_same_thread': False})

# Postgres
SQLALCHEMY_DATABSE_URL = 'postgresql://postgres:adminadmin@localhost/todo-db'
engine = create_engine(SQLALCHEMY_DATABSE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() 


def get_db():
    db = SessionLocal()
    try:

        yield db        # Returns first then continues to close connection.
    finally:
        db.close()