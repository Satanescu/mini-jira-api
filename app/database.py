from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

#Connection string from docker-compose
DATABASE_URL = os.environ.get("DATABASE_URL")

#create engine -> conect to postgresql
engine = create_engine(DATABASE_URL)

#create a session class to talk to the DB in each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#create the base class??
Base = declarative_base()