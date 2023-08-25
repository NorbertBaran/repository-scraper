import logging
import time
from src.database.shemas import *
from src.database.engine import engine, Base

logging.basicConfig(level=logging.DEBUG)
logging.info("Creating database schema")

connected = False
while connected == False:
    try:
        logging.info("Database engine connecting...")
        connection = engine.connect()
        connected = True
        logging.info("Database connected successfully!")
        connection.close()
        if not engine.dialect.has_table(engine.connect(), 'repositories'):
            Base.metadata.create_all(engine)
            logging.info("Database created successfully!")
        else:
            logging.info("Database already exists!")
                
    except Exception as e:
        logging.info("Database connection failed.")
        time.sleep(1)
