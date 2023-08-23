import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES = os.environ.get("POSTGRES_CONNECTION")

engine = create_engine(POSTGRES)
Base = declarative_base()
Session = sessionmaker(bind=engine)