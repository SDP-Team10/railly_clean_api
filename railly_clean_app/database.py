import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = os.environ["DATABASE_URL"]
db_url_fixed = "postgresql+psycopg2://" + db_url.split("://")[1]
SQLALCHEMY_DATABASE_URL = db_url_fixed

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
