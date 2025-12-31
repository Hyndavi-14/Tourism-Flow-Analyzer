# db.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# load .env file
load_dotenv()

def get_engine():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")      # RDS endpoint
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")      # your DB name (tourism_project)

    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)
    return engine
