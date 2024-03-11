# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')

DATABASE_URL = f"postgresql://{db_username}:{db_password}@db/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)