
import databases
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config("DATABASE_URL")

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

engine = create_engine(
	DATABASE_URL,
	# connect_args={"check_same_thread": True}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
