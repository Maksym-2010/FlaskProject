import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


DATABASE = create_engine(os.getenv("DATABASE"))

Session = sessionmaker(DATABASE)
session = Session()

BASE = declarative_base()


def create_db():
    BASE.metadata.create_all(DATABASE)
