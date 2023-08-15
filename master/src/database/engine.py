import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION")

engine = create_engine(DATABASE_CONNECTION)
Base = declarative_base()
Session = sessionmaker(bind=engine)